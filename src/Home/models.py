# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from taggit.models import Tag

from django.db import models


class BlogIndex(models.Model):
    pass


class Contact(models.Model):
    tag_query = (
        ('Account and publish issues', 'مشاكل الحساب و النشر'),
        ('Rules violence', 'الإبلاغ عن انتهاك للقواعد'),
        ('DMCA and Copyright', 'قضايا DMCA / حقوق الطبع والنشر'),
        ('FeedBack and other', 'ردود الفعل أو مشاكل أخرى'),
    )

    tag = models.CharField(choices=tag_query,default=tag_query[0][0],blank=False, max_length=300)
    email = models.EmailField(default='', blank=False)
    subject = models.CharField(default='', blank=False, max_length=2000)

    def __str__(self):
        return self.tag