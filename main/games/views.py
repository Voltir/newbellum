from django.views.generic import ListView, DetailView
from games.models import Game

class GamesView(ListView):
    '''View and interact with all of the games'''
    
    template_name = 'games/index.html'
    model = Game
    
    def get_context_data(self, **kwargs):
        context = super(GamesView,self).get_context_data(**kwargs)
        for thisGame in context['game_list']:
            membership = thisGame.get_membership(self.request.user)
            if membership:
                thisGame.is_member = True
                thisGame.joined_date = membership.date
            else:
                thisGame.is_member = False

        return context
    
class GameDetailView(DetailView):
    template_name = 'games/game_detail.html'
    model = Game
    
