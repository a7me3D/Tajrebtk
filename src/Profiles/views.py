# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.shortcuts import render, HttpResponseRedirect
from .forms import EditProfileForm, EditUserProfileForm, CustomLoginForm, CustomSignup
from .models import UserProfile
from plateform.models import BlogPost as posts
from django.shortcuts import reverse
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin
from allauth.socialaccount.helpers import SocialLogin
from allauth.account.utils import messages

from allauth.socialaccount.views import SignupView as SocialSignupView


class CustomSocialSignupView(SocialSignupView):
    def dispatch(self, request, *args, **kwargs):
        self.sociallogin = None
        data = request.session.get('socialaccount_sociallogin')
        if data:
            self.sociallogin = SocialLogin.deserialize(data)
        if not self.sociallogin:
            return HttpResponseRedirect(reverse('portal'))

        # if exists account with same email, redirect to login page with message
        user_email = self.sociallogin.user.email
        try:
            user = User.objects.get(email=user_email)
            messages.error(request, (
                'للاسف لم تتمكن من تسجيل دخولك عبر الفايسبوك البريد الالكتروني المستخدم مسجل بحساب آخر من قبل يرجى انشاء حساب او تسجيل الدخول'),
                           extra_tags='safe')
            return HttpResponseRedirect(reverse('portal'))
        except User.DoesNotExist:
            return super(SignupView, self).dispatch(request, *args, **kwargs)


class CustomSignupView(SignupView, AjaxCapableProcessFormViewMixin):
    # here we add some context to the already existing context
    def get_context_data(self, **kwargs):
        # we get context data from original view
        context = super(CustomSignupView,
                        self).get_context_data(**kwargs)
        context['login_form'] = CustomLoginForm()  # add form to context
        context['form'] = CustomSignup()
        return context


def profile(request, username):
    user = User.objects.get(username=username)
    related = posts.objects.filter(author=user)
    args = {
        'user': user,
        'related': related
    }
    return render(request, 'profile/profile.html', args)


@login_required(login_url='/accounts/portal')
def edit_profile(request):
    user = request.user
    user_form = EditProfileForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, form=EditUserProfileForm, can_delete=False)
    formset = ProfileInlineFormset(instance=user)
    if request.user == user:
        if request.method == "POST":
            user_form = EditProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            created_user = user_form.save(commit=False)

            if formset.is_valid() and user_form.is_valid():
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                created_user.save()
                formset.save()
                return HttpResponseRedirect('/accounts/u/' + user.username)
                
        return render(request, "profile/user_update.html",
                      {"user_form": user_form, 'formset': list(formset[0]), 'management': formset.management_form})
