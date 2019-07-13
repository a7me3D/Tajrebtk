# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import string
from urllib.parse import quote_plus
import jinja2.utils
from django.contrib.auth.admin import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _
from froala_editor.fields import FroalaField
from taggit.models import Tag
from django.core.urlresolvers import reverse


from .validation import *
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment

class BlogPosts(models.Model):
    pass


@python_2_unicode_compatible
class BlogPost(models.Model):
    #Post Detail
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    title = models.CharField(default=None, max_length=50, unique=True, validators=[is_title])
    body = FroalaField(default="", validators=[is_body])
    description = models.CharField(default='',max_length=200, validators=[is_desc])
    source = models.URLField(default='', validators=[is_url])
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, default='', validators=[is_tag])
    slug = models.CharField(_('Slug'), max_length=300, blank=True, default='')
    date = models.DateTimeField(default=datetime.datetime.now)
    keys = models.CharField(max_length=300, blank=False, default='',validators=[is_key])
    anonymous = models.BooleanField(default=False)
    #thumb
    post_cover_original = models.ImageField(upload_to="original_cover", null=True, validators=[is_valid_image])
    post_cover_thumb = models.ImageField(upload_to='thumb_cover', null=True, blank=True)
    #hits
    hits = models.IntegerField(default=0)
    #comments
    comments = GenericRelation(Comment)
    #like
    liked = models.ManyToManyField(User, related_name='PostLikeToggle')


    def get_absolute_url(self):
        return reverse("posts:BlogPost", kwargs={"slug": self.slug})

    # formattig the slug (security things)
    def slugy(self,text):
        safe = string.punctuation
        for i in text:
            if i in safe:
                text = text.replace(i, jinja2.utils.escape(quote_plus(i)))
        text = text.replace(' ', '_')
        return text
    # todo :if len(desc)= 0 trancate desc from body

    def desc(self,desc):
        return desc

    def save(self, *args, **kwargs):

        if not self.id:
            # Only set the slug when the object is created.
            self.slug = self.slugy(self.title)
            super(BlogPost, self).save(*args, **kwargs)
            from django.utils.crypto import get_random_string
            from PIL import Image

            org_path = str(self.post_cover_original.path)
            try:
                fname = org_path.rsplit('\\', 1)[1].rsplit('.', 1)[0]
                fullpath = org_path.rsplit('\\', 1)[0]
            except:
                fname = org_path.rsplit('/', 1)[1].rsplit('.', 1)[0]
                fullpath = org_path.rsplit('/', 1)[0]
            randomstr = get_random_string(length=7)

            def thumbnailize(image):
                n_size = 500, 500
                im = Image.open(image)
                im.thumbnail(n_size)
                # add blog title to image path
                try:
                    im.save(fullpath.rsplit('\\', 1)[0] + '\\thumb_cover\\' + fname + '_' + randomstr + '_thumb.png')
                    print("thumbnail saved")
                except:
                    im.save(fullpath.rsplit('/', 1)[0] + '\\thumb_cover\\' + fname + '_' + randomstr + '_thumb.png')

                im.close()

            thumbnailize(self.post_cover_original)
            self.post_cover_thumb = "thumb_cover\\" + fname + '_' + randomstr + '_thumb.png'
            super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

