# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import string
from urllib import quote_plus

from django.core.validators import ValidationError, URLValidator
from jinja2.filters import do_striptags, do_wordcount
from jinja2.utils import escape
from taggit.models import Tag

err_ar = 'الحروف اللاتينية غير مسموحة'


# todo: validate image dimension
def is_valid_image(image):
    if image:
        org_path = str(image.path)
        try:
            ext = org_path.rsplit('\\', 1)[1].rsplit('.', 1)[1]
        except:
            ext = org_path.rsplit('/', 1)[1].rsplit('.', 1)[1]

        try:
            from PIL import Image
            Image.open(image)
            if len(ext) == 0:
                raise ValidationError('خلل عند الرفعة,يرجى التاكد من الصورة')
            elif str(ext.lower()) not in ['jpe', 'jpg', 'mpeg', 'jpeg', 'tif', 'gif', 'mpg', 'bmp', 'png', 'tiff']:
                raise ValidationError(ext + ' غير مدعوم ')
        except IOError:
            raise ValidationError('خلل عند الرفع,يرجى التاكد من الصورة')
    else:
        raise ValidationError('لم ترفع صورة العرض', code='required')
    return image


def is_tag(tag):
    all_tags = [i.id for i in Tag.objects.all()]
    if not tag in all_tags:
        raise ValidationError(str(tag), 'غير موجود')
    return tag


def slugy(text):
    safe = string.punctuation
    for i in text:
        if i in safe:
            text = text.replace(i, escape(quote_plus(i)))
            text = text.replace(' ', '_')
            return text


def is_title(title):
    import re
    from .models import BlogPost
    slug = slugy(title)
    if title is None or title == "":
        msg = 'يبدو انك نسيت كتابة الموضوع'
        return msg
        raise ValidationError(msg)
    if BlogPost.objects.filter(title__iexact=title) or BlogPost.objects.filter(slug__iexact=slug):
        msg = 'تم استخدام هذا العنوان من قبل,الرجاء تغييره'
        return msg
        raise ValidationError(msg)
    match = re.compile(r'^[ء-ي\s\W\d]+$')
    if match.findall(title):
        if match.findall(title)[0] != title:
            return err_ar.encode('utf-8')
            raise ValidationError(err_ar)
    else:
        return err_ar.encode('utf-8')
        raise ValidationError(err_ar)
    return title


def is_body(body):
    safe_body = do_striptags(body)
    if do_wordcount(safe_body) < 100:
        msg = 'روايتك مختصرة حاول اضافة بعض التفاصيل ' + ' \n' + str(
            do_wordcount(safe_body)) + ' كلمة مستعملة , 100 للحد الادنى '
        return msg
        raise ValidationError(msg)
    return body


def is_key(keys):
    import re
    import string
    match = re.compile(r'^[ء-ي\s]+$')
    safe = string.punctuation
    for i in keys:
        if i in safe:
            keys = keys.replace(i, ' ')
    if match.findall(keys):
        if keys != match.findall(keys)[0]:
            raise ValidationError(err_ar)
    else:
        raise ValidationError(err_ar)
    return keys


def is_desc(desc):
    import re
    match = re.compile(r'^[ء-ي\s\W\d]+$')
    if len(desc):
        if match.findall(desc):
            if desc != match.findall(desc)[0]:
                raise ValidationError(err_ar)
        else:
            raise ValidationError(err_ar)
        safe_desc = do_striptags(desc)
        if do_wordcount(safe_desc) < 30:
            msg = 'وصف قصير 30 كلمة الحد الادنى' + str(do_wordcount(safe_desc)) + ' كلمة مدخلة'
            raise ValidationError(msg)
    return desc


class is_url(URLValidator):
    message = 'يرجى التاكد من ادخال رابط صحيح'
