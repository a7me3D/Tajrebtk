# -*- coding: utf-8 -*-


from django.core.validators import ValidationError
from django.contrib.auth.models import User
import re


def is_username(username):
    match = re.compile(u'^[ء-ي\w\d]+$')
    if User.objects.filter(username=username):
        raise ValidationError('اسم المستخدم مسجل مسبقا')
    if len(match.findall(username)) == 0:
        raise ValidationError('الحروف و الارقام و _ فقط')
    return username

UsernameValidators = [is_username]

def is_fname(fname):
    match = re.compile(u'^[ء-يa-zA-Z]+$')
    if len(match.findall(fname)) == 0:
        raise ValidationError('الحروف فقط مسموحة ')
