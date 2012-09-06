from django.conf.urls import patterns, include, url

urlpatterns = patterns('news.views',
    url(r'^$', 'index'),
    url(r'^submit/', 'submit'),
    url(r'^submitted/', 'submitted'),
)