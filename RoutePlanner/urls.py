from django.conf.urls import patterns, url
from RoutePlanner import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
)