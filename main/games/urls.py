from django.conf.urls import patterns, include, url
from games.views import GamesView, GameDetailView

urlpatterns = patterns('games.views',
    url(r'^$', GamesView.as_view()),
    url(r'^(?P<pk>\d+)/$', GameDetailView.as_view(), name='game_detail_view'),
)
