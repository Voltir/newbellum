from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from news.models import NewsItem, Topic
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from guardian.mixins import LoginRequiredMixin

from forms import NewsForm

#See:
# https://docs.djangoproject.com/en/dev/topics/class-based-views/
# http://stackoverflow.com/questions/5907575/how-do-i-use-pagination-with-django-class-based-generic-listviews
#--Volt
class NewsItemView(ListView):
    template_name = 'news/index.html'
    model = NewsItem
    context_object_name = 'news_items'
    paginate_by = 3

    def get_queryset(self):
        return NewsItem.objects.filter(published=True).order_by('-post_time')

#http://stackoverflow.com/questions/5607205/how-can-i-make-a-generic-class-based-create-view-for-a-model
#TODO: Create login functionality so this doesnt 404 if not authenticated
#--Volt
class NewsItemCreate(LoginRequiredMixin,CreateView):
    template_name = 'news/submit.html'
    model = NewsItem
    form_class = NewsForm

    def form_valid(self,form):
        self.news_item = form.save(commit=False)
        self.news_item.submitter = self.request.user
        self.news_item.save()
        return HttpResponseRedirect('/news/submitted')
