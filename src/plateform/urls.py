from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.BlogPosts, name='BlogPosts'),
    url(r'^article/(?P<slug>[\w\W]*)', views.BlogPost,  name='BlogPost'),
    # url(ur'^article/(?P<slug>[\w\W]*)', views.BlogPost,  name='BlogPost'),
    url(r'^new/$', views.Editor, name='Editor'),
    url(r'^posts/$', views.update_posts, name='Posts'),


]