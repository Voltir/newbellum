from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from news.models import NewsItem, Topic, NewsForm
from django.template import RequestContext
from django.contrib.auth.models import User

def get_user_object(request):
    if  request.user.is_anonymous():
        return get_anonymous_user()
    else:
        return request.user

def index(request):
    #TODO:  Pagination
    n = NewsItem.objects.filter(published=True).order_by('-post_time')
    return render_to_response('news/index.html', {'newsitems': n})

def submit(request):
    f = NewsForm(request.POST)
    user = get_user_object(request)
    if f.is_valid():
        if request.user.is_authenticated() and user == request.user:
            # Save Stuff
            n = NewsItem()
            n.title = f.cleaned_data['title']
            n.body = f.cleaned_data['message']
            n.topic = Topic.objects.get(pk=f.cleaned_data['topic'])
            n.submitter = user
            n.save()
            #TODO: Send Notification E-mail
            return HttpResponseRedirect('/news/submitted')
        else:
            return HttpResponseRedirect('/')
    else:
        f = NewsForm()
        
    csrfContext = RequestContext(request, {'form': f,})
    return render_to_response('news/submit.html', csrfContext)

def submitted(request):
    return render_to_response('news/submitted.html')