from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import *

urlpatterns = patterns('profile.views',
    url(r'^create/', ProfileCreate.as_view()),
    url(r'^test/', test_view),
)
