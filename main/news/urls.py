from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from news.forms import NewsFormPreview, NewsForm

from views import *

urlpatterns = patterns('news.views',
    url(r'^$', NewsItemView.as_view()),
    url(r'^submit/', NewsFormPreview(NewsForm)),
    url(r'^preview/', NewsFormPreview(NewsForm)),
    url(r'^preview_html/', 'NewsPreviewHTML'),
    url(r'^submitted/', TemplateView.as_view(template_name='news/submitted.html')),
)
