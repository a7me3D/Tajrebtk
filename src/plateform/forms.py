# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from froala_editor.widgets import FroalaEditor
from jinja2.utils import generate_lorem_ipsum
from taggit.models import Tag
from .models import BlogPost

Tags = Tag.objects.all()


class PostForm(forms.ModelForm):


    body = forms.CharField(initial=generate_lorem_ipsum(1, min=100, max=1000), label='',
                           widget=FroalaEditor(theme="royal", options={'toolbarInline': False, },
                                               attrs={'class': 'editor_body'}))
    title = forms.CharField(label='',
                            widget=forms.TextInput(attrs={
                                'id': 'title',
                                'placeholder': 'ماهو موضوع اليوم'}))

    tags = forms.ModelChoiceField(queryset=Tags, widget=forms.Select(attrs={'class': 'wide'}),
                                  empty_label=None, label='', required=False)

    description = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'class': 'desc',
                                                                                         'placeholder': 'ادخل هنا مقدمة قصير او خلاصة للموضوع \n\n سيتم اخذ الفقرة الاولى ان بقي هذا الحقل فارغا'}))

    keys = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'ادخل كلمات دلالية مناسبة',
        'class': 'slug'}))

    source = forms.CharField(required=False, widget=forms.URLInput(attrs={'class': "src", "placeholder": "http://"}),
                             error_messages={"invalid": "يرجى التاكد من ادخال رابط صحيح"})

    post_cover_original = forms.FileField('posts_thumb', label='', error_messages={'required': 'لم ترفع صورة العرض'})

    anonymous = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(),
                                   label='لا اريد نشر هويتي')

    class Meta:
        model = BlogPost
        fields = ('title', 'tags', 'body', 'keys', 'anonymous', 'post_cover_original', 'description', 'source')


from comments.forms import CommentForm


class Custom_CommentForm(CommentForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 512}), max_length=512)
