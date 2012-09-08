from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from guardian.mixins import LoginRequiredMixin

from models import Profile

class ProfileCreate(LoginRequiredMixin,CreateView):
    template_name = 'site_profile/create.html'
    model = Profile
    success_url = 'profile/test/'


#this is just hackery to verify what django does...
#using one-one field lets you do things like this..
#(notice djangobb_forum is not imported, but i still can access the forum profile)
#now im not sure what to do about site profiles...
def test_view(request):
    print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",request.user.profile.pledged
    print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",request.user.forum_profile
    return HttpResponseRedirect('/forum/')
