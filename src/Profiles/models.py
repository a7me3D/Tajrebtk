# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from .validators import *


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    first_name = models.CharField(default='', max_length=100, validators=[is_fname])
    last_name = models.CharField(default='', max_length=100, validators=[is_fname])
    email = models.EmailField(max_length=100, blank=False, default='')
    avatar = ImageField('صورة المستخدم', default='avatars/alien.png', upload_to="avatars", )
    bio = models.CharField('عن المستخدم', blank=True, default='', max_length=200)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)

from allauth.account.signals import user_logged_in
from allauth.socialaccount.helpers import SocialLogin
from allauth.socialaccount.helpers import _add_social_account


@receiver(user_logged_in, dispatch_uid="allauth.account.signals.user_logged_in")
def auto_connect_social_account(request, user, **kwargs):
    """
    If user sucessfully login via social network, but he already has account (based on email),
    he is provoke to login via email. After logged in, this signal create connection between social network and user account.
    Next time user can use social network or email to login.
    """

    sociallogin = None
    data = request.session.get('socialaccount_sociallogin', None)
    if data:
        sociallogin = SocialLogin.deserialize(data)

    if not sociallogin:
        return

    if user.email != sociallogin.user.email:
        return

    _add_social_account(request, sociallogin)

    del request.session['socialaccount_sociallogin']


from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.account import app_settings


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(request, users[0], email_verification=app_settings.EMAIL_VERIFICATION)
