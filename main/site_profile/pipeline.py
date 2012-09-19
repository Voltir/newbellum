from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

def check_registration(backend, user, uid, request, social_user=None, *args, **kwargs):
    if "saved_username" not in request.session and user is None:
        print "Do this thing.."
        request.session["authentication_backend"] = backend.name
        request.session["authentication_uid"] = uid
        return HttpResponseRedirect("/registration/")

def username(user,request,*args,**kwargs):
    if user:
        username = user.username
    else:
        username = request.session["saved_username"]
    return {'username':username}

def test_wat(backend, user, uid, social_user=None, *args, **kwargs):
    return {'username':"FooBar"}
