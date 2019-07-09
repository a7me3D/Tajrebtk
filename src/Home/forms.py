# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django import forms

from .models import Contact

tag_query = (
    ('Account and publish issues', 'مشاكل الحساب و النشر'),
    ('Rules violence', 'الإبلاغ عن انتهاك للقواعد'),
    ('DMCA and Copyright', 'قضايا DMCA / حقوق الطبع والنشر'),
    ('FeedBack and other', 'ردود الفعل أو مشاكل أخرى'),
)


class ContactForm(forms.ModelForm):
    tag = forms.ChoiceField(label='القسم', choices=tag_query,
                            widget=forms.Select(attrs={'class': 'wide', 'id': 'id_tags', 'name': 'tags'}),
                            required=False)
    email = forms.EmailField(label='البريد الالكتروني', required=True)
    subject = forms.CharField(label='وصف الموضوع', widget=forms.Textarea(attrs={'rows':80,'cols':5}), required=True, max_length=2000)

    class Meta():
        model = Contact
        fields = '__all__'
