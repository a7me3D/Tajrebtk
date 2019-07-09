# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import ContactForm
import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse



# Create your views here.
def BlogIndex(request):
    return render(request, "tmp_blog_index.html", {})


def Contact(request):
    meta = None
    if request.user.is_authenticated():
        meta = request.user
    Form = ContactForm(instance=meta)

    if request.method == 'POST':
        Form = ContactForm(request.POST, instance=meta)
        if Form.is_valid():
            Form = ContactForm(request.POST, instance=meta)
            Form.save()
            resp = {'status': '200'}
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            data = {
                'errors':Form.errors
            }
            print Form.errors
            return JsonResponse(data,status=400)

    args = {
        'Form': Form
    }
    return render(request, 'contact.html', args)
