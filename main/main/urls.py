from django.conf.urls import patterns, include, url
from django.contrib.auth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import djangobb_forum 
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testing.views.home', name='home'),
    # url(r'^testing/', include('testing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forum/', include('djangobb_forum.urls',namespace="djangobb")),
    #url(r'^account/login/$',  login),
    #url(r'^account/logout/$', logout),
    #url(r'^account/password_change/$', password_change, name="auth_password_change"),
    #url(r'^account/password_change/done/$', password_change_done),
    #url(r'^grappelli/',include('grappelli.urls')),
)