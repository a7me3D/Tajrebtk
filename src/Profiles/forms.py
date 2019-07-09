# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.admin import User
from django.contrib.auth.forms import UserChangeForm
from django.core import validators
from .models import UserProfile


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم', widget=forms.TextInput(attrs={'placeholder': 'الاسم'}))
    last_name = forms.CharField(label='اللقب', widget=forms.TextInput(attrs={'placeholder': 'اللقب'}))
    rules = forms.BooleanField(label='أوافق على شروط الموقع', error_messages={'required': ' لم توافق على شروط الموقع'})

    class Meta:
        model = UserProfile
        exclude = ('user', 'avatar', 'cover', 'bio')
        field_order = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rules')

    def signup(self, request, user):
        self.username = self.cleaned_data['username']
        user.userprofile.first_name = self.cleaned_data['first_name']
        user.userprofile.last_name = self.cleaned_data['last_name']
        user.userprofile.email = self.cleaned_data['email']
        user.userprofile.save()
        user.save()


from allauth.account.forms import SignupForm
from allauth import app_settings
from allauth.utils import get_user_model
from allauth.account.utils import get_adapter, user_email, user_username


class CustomSignup(SignupForm):
    username = forms.CharField(label="Username",
                               min_length=3,
                               widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'autofocus': 'autofocus'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'email',
               'placeholder': 'البريد الالكتروني'}))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(label="كلمة السر")
        self.fields['password2'] = PasswordField(label='تاكيد كلمة السر')

        if hasattr(self, 'field_order'):
            set_form_field_order(self, self.field_order)


from allauth.account.forms import LoginForm, PasswordField
from allauth.utils import set_form_field_order


class CustomLoginForm(LoginForm):
    password = PasswordField(label="كلمة السر")
    remember = forms.BooleanField(label="تذكرني",
                                  required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
        login_widget = forms.TextInput(attrs={'placeholder': 'اسم المستخدم'})
        login_field = forms.CharField(
            label="اسم المستخدم",
            widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])


from .validators import *
from django.core.validators import EmailValidator


class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=10, label='اسم المستخدم', help_text='')
    email = forms.EmailField(label='البريد الالكتروني', widget=forms.TextInput(attrs={"size": 50}),
                             validators=[EmailValidator])
    first_name = forms.CharField(label='الاسم', validators=[is_fname])
    last_name = forms.CharField(label='اللقب', validators=[is_fname])
    password = None

    def clean_username(self):
        match = re.compile(u'^[ء-ي\w\d]+$')
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exclude(username=self.instance.username):
            raise ValidationError('اسم المستخدم مسجل مسبقا')
        if len(match.findall(username)) == 0:
            raise ValidationError('الحروف و الارقام و _ فقط')
        return username

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')





class EditUserProfileForm(forms.ModelForm):

    bio = forms.CharField(label='عن المستخدم', widget=forms.Textarea(attrs={'maxlength': 200, 'rows': 3}), required=False)
    avatar = forms.ImageField(label_suffix='avatar', widget=forms.FileInput(attrs={'hidden': '', }))

    class Meta():
        model = UserProfile
        fields = ('avatar', 'bio',)
