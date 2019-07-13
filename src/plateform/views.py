# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import json
import re
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from el_pagination.decorators import page_template
from .forms import PostForm
from .models import BlogPost as posts
from .validation import is_body, is_title


def _sugg():
    sugg = []
    filters = [posts.objects.filter(tags__name='تجارب شخصية'), posts.objects.filter(tags__name='ثقافات'),
               posts.objects.filter(tags__name='تكنلوجيا')]
    for tag in filters:
        tag = tag.order_by('hits')[:2]
        for post in tag:
            sugg.append(post)
    return sugg


@page_template('posts_index.html')
def BlogPosts(request, template="blog_posts.html", extra_context=None):
    context = {
        'posts_count': posts.objects.all().count(),
        'blogpages': posts.objects.all().order_by('date'),
        'sugg': _sugg()
    }
    if request.is_ajax() and not ('tag' in request.POST.keys() or 'search' in request.POST.keys()):
        context.update(extra_context)

    return render(request, template, context)

from random import randrange
def update_posts(request, template='posts_index.html'):
    context = {
        'blogpages': posts.objects.all(),
        'posts_count': posts.objects.all().count(),
    }
    if request.method == 'POST':
        if 'tag' in request.POST.keys():
            tag = request.POST['tag']
            context['blogpages'] = posts.objects.filter(tags__name=tag)
            if tag == 'الاحدث ':
                context['blogpages'] = posts.objects.order_by('date')

        if 'search' in request.POST.keys():
            search = request.POST.get('search')
            context['blogpages'] = posts.objects.filter(title__contains=search)
    if request.method == 'GET':
        if request.is_ajax():
            BlogPost_url = reverse('BlogPost',kwargs={'slug':context['blogpages'][randrange(1,(context['posts_count']))].slug})
            return JsonResponse({'lucky':BlogPost_url},status=200)

    return render(request, template, context)


from Profiles.models import UserProfile  as Author
from django.contrib.auth.models import User
from random import sample

def _related(tag):
    related_posts = list(posts.objects.filter(tags__name=tag))

    related = sample(related_posts, min(max(0,len(related_posts)),3))
    return related


def BlogPost(request, slug=None):
    post_slug = get_object_or_404(posts, slug=slug)
    user = request.user
    _liked = user in post_slug.liked.all()
    author_avatar = Author.objects.get(user=User.objects.get(username=post_slug.author).id)
    args = {
        'post_slug': post_slug,
        'author_avatar': author_avatar,
        'related': _related(post_slug.tags),
        'liked':_liked,
    }

    # request.META['HTTP_X_FORWARDED_FOR']
    ip = '127.0.0.1'
    visited = cache.get(ip)
    if not visited:
        post_slug.hits += 1
        cache.set(ip, True)

    return render(request, "blog_post.html", args)


# Articles Like Function view
def PostLikeToggle(request):
    user = request.user
    if user.is_authenticated():

        if request.method == 'POST':
            post_id = request.POST['post_id']
            post = get_object_or_404(posts, id=post_id)
            _liked = user in post.liked.all()
            if _liked:
                post.liked.remove(user)
            else:
                post.liked.add(user)
            return JsonResponse({'liked': _liked})
        else:
            return HttpResponse()
    else:
        return HttpResponse('you need to login')


@login_required(login_url='/accounts/portal')
def Editor(request):
    if re.search('(msie\s)|(trident)|(edge)', request.META['HTTP_USER_AGENT'].lower()):
        return render(request, 'IE-NotSupported.html')
    else:
        post_form = PostForm
        if request.method == "POST":
            if request.is_ajax() and 'next' in request.POST.keys():
                title = request.POST['title']
                body = request.POST['body']
                data = {}
                if title == is_title(title) and body == is_body(body):
                    return JsonResponse(data, status=200, safe=False)
                else:
                    if not (title == is_title(title)):
                        data.update({'ErrTitle': is_title(title)})
                    if not (body == is_body(body)):
                        data.update({'ErrBody': is_body(body)})
                    print(json.dumps(data))
                    return JsonResponse(data, status=400, safe=False)

            if request.is_ajax():
                post_form = PostForm(request.POST, request.FILES)
                if post_form.is_valid():
                    print('form is valid')
                    created_post = post_form.save(commit=False)
                    post_form = PostForm(request.POST, request.FILES, instance=created_post)
                    created_post.title = request.POST['title']
                    created_post.body = request.POST['body']
                    created_post.author = request.user
                    created_post.save()
                    resp = {'status': '200'}
                    return HttpResponse(json.dumps(resp), content_type='application/json')
                else:
                    data = {
                        'errors': post_form.errors
                    }
                    print(data)
                    return JsonResponse(data, status=400)
        else:
            post_form = PostForm()
        data = {'editor': post_form}
        return render(request, 'writer.html', data)


from comments.views import CommentCreateView
from .forms import Custom_CommentForm
from comments.models import Comment, Like
from django.core.urlresolvers import reverse_lazy,reverse
from django.contrib.contenttypes.models import ContentType


class Custom_CommentCreateView(CommentCreateView):
    form_class = Custom_CommentForm
    model = Comment
    template_name = 'comments/comment_form.html'
    success_url = reverse_lazy('comment-create')

    def form_valid(self, form):
        comment = form.save(commit=False)
        try:
            content_type = ContentType.objects.get(
                app_label=self.request.POST['app_name'],
                model=self.request.POST['model'].lower())
            model_object = content_type.get_object_for_this_type(
                id=self.request.POST['model_id'])
            comment.content_object = model_object
        except:
            pass

        comment.save()
        return super(Custom_CommentCreateView, self).form_valid(form)


# Comments Like Function view
from comments.views import LikeComment


class Custome_LikeComment(LikeComment):
    def get(self, request, *args, **kwargs):
        comment_id = request.GET.get('comment_id')
        likes_count = 0
        data = {}

        # Check if user is authenticated.
        if not request.user.is_authenticated():
            # Return if user is not authenticated.
            data['success'] = 0
            data['error'] = "You have to sign in first"
            return JsonResponse(data)

        user = request.user
        try:
            # Check if the comment with the requested id exists.
            comment = Comment.objects.get(id=comment_id)
            likes_count = comment.likes_count
            try:
                # Check if the user already liked the comment,
                # Do nothing in this case.
                Like.objects.get(comment=comment, user=user)
                data['success'] = 0
                data['error'] = "You have already liked this comment"
            except:
                # Create a like on the comment in case the user hasn't
                # liked it already.
                Like.objects.create(comment=comment, user=user).save()
                likes_count += 1
                comment.likes_count = likes_count
                comment.save()
                data['likes_count'] = likes_count
                data['success'] = 1
        except:
            # Return an error where the comment might have been removed.
            data['success'] = 0
            data['error'] = "This comment might have been removed"
        return JsonResponse(data)
