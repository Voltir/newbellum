from django.conf.urls import patterns, include, url
from games.views import GamesView, GameDetailView

urlpatterns = patterns('games.views',
    url(r'^$',                    GamesView.as_view(),        name='game_list'),
    url(r'^(?P<pk>\d+)/$',        GameDetailView.as_view(),   name='game_detail_view'),
    url(r'^(?P<pk>\d+)/join/$',  'game_join',                 name='game_join'),
    url(r'^(?P<pk>\d+)/leave/$', 'game_leave',                name='game_leave'),
)
