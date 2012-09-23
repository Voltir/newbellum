from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from games.models import Game, GameMember

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
    
    def get_context_data(self, **kwargs):
        context = super(GameDetailView,self).get_context_data(**kwargs)
        thisGame = context['game']
        membership = thisGame.get_membership(self.request.user)
        if membership:
            thisGame.is_member = True
            thisGame.joined_date = membership.date
        else:
            thisGame.is_member = False

        return context
    
def game_join(request, pk):
    game = get_object_or_404(Game, pk=pk)
    user = request.user
    if GameMember.objects.filter(game=game,user=user).count() == 0:
        print "Adding Member"
        m = GameMember()
        m.game = game
        m.user = user
        m.save()
        
    return redirect('game_detail_view',pk=pk)

def game_leave(request, pk):
    game = get_object_or_404(Game, pk=pk)
    user = request.user
    if GameMember.objects.filter(game=game,user=user).count() == 1:
        print "Removing Member"
        GameMember.objects.filter(game=game,user=user).delete()
        
    return redirect('game_list',pk=pk)
    