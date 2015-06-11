from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import patterns, url
from RoutePlanner import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MegaByke.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^RoutePlanner/', include('RoutePlanner.urls')),
)
