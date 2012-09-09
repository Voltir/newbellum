from django.contrib.formtools.preview import FormPreview
from django import forms
from news.models import NewsItem,Topic
from django.contrib.auth.models import User
from djangobb_forum.util import smiles, convert_text_to_html
from datetime import datetime
from django.http import HttpResponseRedirect

class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ('title','topic','body')
        
class NewsFormPreview(FormPreview):
    form_template = 'news/submit.html'
    preview_template = 'news/preview.html'
    
    def process_preview(self, request,  form, context):
        context['newsitem'] = form.save(commit=False)
        context['newsitem'].body_html = convert_text_to_html(form.cleaned_data['body'], "bbcode") 
        context['newsitem'].body_html = smiles(context['newsitem'].body_html )
        context['newsitem'].submitter_username = request.user.username
        context['newsitem'].post_time = datetime.now()
        print "Form Valid?: ", form.is_valid()
        
    def done(self, request, cleaned_data):
        ni = NewsItem()
        ni.topic = cleaned_data['topic']
        ni.body = cleaned_data['body']
        ni.title = cleaned_data['title']
        ni.submitter = request.user
        ni.save()
        return HttpResponseRedirect('/news/submitted')
