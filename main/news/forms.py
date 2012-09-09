from django.contrib.formtools.preview import FormPreview
from django import forms
from news.models import NewsItem,Topic
from django.contrib.auth.models import User
from djangobb_forum.util import smiles, convert_text_to_html

class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ('title','topic','body')
        
class NewsFormPreview(FormPreview):
    form_template = 'news/submit.html'
    preview_template = 'news/preview.html'
    
    def process_preview(self, request,  form, context):
        self.news_item = form.save(commit=False)
        form.body_html = convert_text_to_html(form.cleaned_data['body'], "bbcode") 
        form.body_html = smiles(form.body_html)
        #form.topic_image = form.topic.topic_image
        form.topic_image = self.news_item.topic_image
        form.sumbmitter_username = self.requst.user.username
        
    def done(self, request, cleaned_data):
        self.news_item = form.save(commit=False)
        self.news_item.submitter = self.request.user
        self.news_item.save()
        return HttpResponseRedirect('/news/submitted')
