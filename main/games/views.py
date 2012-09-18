from django.views.generic import ListView, DetailView
from games.models import Game

class GamesView(ListView):
    '''View and interact with all of the games'''
    
    template_name = 'games/index.html'
    model = Game
    
class GameDetailView(DetailView):
    template_name = 'games/game_detail.html'
    model = Game
    
    
#    def get_context_data(self, **kwargs):
#        context = super(GameDetailView,self).get_context_data(**kwargs)
#        context['game'] = Game.objects.get(pk=context['params']['pk'])
#        print str(context)
#        return TemplateView.get_context_data(self, **kwargs)