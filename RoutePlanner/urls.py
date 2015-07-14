from django.conf.urls import patterns, url
from RoutePlanner import views, models
import threading

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^route.html$', views.plot_route, name='route'),
        url(r'^register.html$', views.register, name='register'),
        url(r'^login.html$', views.user_login, name='login'),
        url(r'^logout.html$', views.user_logout, name='logout'),
        url(r'^about.html$', views.about, name='about'),
        url(r'^account.html$', views.account, name='account'),
)

from django import setup
setup()