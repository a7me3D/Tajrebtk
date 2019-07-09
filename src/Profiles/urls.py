from django.conf.urls import url, include
from . import views
urlpatterns = [
        url(r'^u/(?P<username>[\-\w]+)/$', views.profile, name='Profile'),
        url(r'^info/change/$', views.edit_profile, name='EditProfile'),
        ]



