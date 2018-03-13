from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^postlist/$', views.post_list, name='post_list'),
    url(r'^$', views.index, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^send/$', views.send, name='send'),
    url(r'^postmaker/$', views.postmaker, name='postmaker'),
    url(r'^postmaker/(?P<group>[0-9]+)/(?P<pk>[0-9]+)/$', views.postmaker, name='postmaker'),
    url(r'^postmaker/next/', views.postmaker, name='postmaker'),
]
