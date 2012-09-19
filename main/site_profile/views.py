from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import *
from django.views.generic.base import *
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout

from models import Profile
from forms import RegistrationForm

class ProfileCreate(LoginRequiredMixin,CreateView):
    template_name = 'site_profile/create.html'
    model = Profile
    success_url = 'profile/test/'

class LoginView(RedirectView):
    url = '/news/'

class LogoutView(RedirectView):
    def get_redirect_url(self):
        auth_logout(self.request)
        return "/forum/"

class RegistrationView(FormView):
    template_name = 'site_profile/registration.html'
    form_class = RegistrationForm
    success_url = '/complete/google/'

    def get_context_data(self, **kwargs):
        ctx = super(FormView,self).get_context_data(**kwargs)
        ctx['auth_backend'] = self.request.session["authentication_backend"]
        ctx['auth_uid'] = self.request.session["authentication_uid"]
        return ctx

    def form_valid(self,form):
        self.request.session["saved_username"] = form.cleaned_data["username"]
        return super(RegistrationView,self).form_valid(form)

#this is just hackery to verify what django does...
#using one-one field lets you do things like this..
#(notice djangobb_forum is not imported, but i still can access the forum profile)
#now im not sure what to do about site profiles...
def test_view(request):
    print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",request.user.profile.pledged
    print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",request.user.forum_profile
    return HttpResponseRedirect('/forum/')
