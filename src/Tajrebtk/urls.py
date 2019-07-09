"""Tajrebtk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from plateform import views as plateform
from Home import views as Home
from Profiles.views import CustomSignupView
from comments.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('plateform.urls'), name='Index'),
    url(r'^blog/', include('plateform.urls'), name='Blog'),
    url(r'^contact/', Home.Contact, name='Contact'),
    url(r'^accounts/', include('Profiles.urls')),
    url(r'^accounts/portal', CustomSignupView.as_view(template_name="account/portal.html"),
        name='portal'),
    url(r'accounts/', include('allauth.urls')),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^blog/writer/$', plateform.Editor, name='Editor'),
    url(r'^like/$', plateform.PostLikeToggle, name='PostLikeToggle'),
    url(r'^comments/like/', plateform.Custome_LikeComment.as_view(), name='comment-like'),
    url(r'^comments/create/$', plateform.Custom_CommentCreateView.as_view(), name='comment-create'),
    url(r'comments/update/(?P<pk>[0-9]+)/$', CommentUpdateView.as_view(), name='comment-update'),
    url(r'^comments/delete/(?P<pk>[-\w]+)$', CommentDeleteView.as_view(), name='comment-delete'),
    url(r'^comments/unlike/$', UnlikeComment.as_view(), name='comment-unlike'),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
