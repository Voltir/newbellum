from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import *

urlpatterns = patterns('news.views',
    url(r'^$', NewsItemView.as_view()),
    url(r'^submit/', NewsItemCreate.as_view()),
    url(r'^submitted/', TemplateView.as_view(template_name='news/submitted.html')),
)
