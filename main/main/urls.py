from django.conf.urls import patterns, include, url
from site_profile.views import LoginView,LogoutView,RegistrationView
from django.contrib.auth.views import *
import djangobb_forum

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$',  login, {'template_name' : 'site_profile/password.html'}, name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^registration/$',  RegistrationView.as_view(), name="registration"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forum/', include('djangobb_forum.urls',namespace="djangobb")),
    url(r'^news/', include('news.urls')),
    url(r'^profile/', include('site_profile.urls')),
    url(r'^games/', include('games.urls')),
    url(r'',include('social_auth.urls')),
    #url(r'^grappelli/',include('grappelli.urls')),
)

# Enable Media Serving when using the Development Server (Rex)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
)

