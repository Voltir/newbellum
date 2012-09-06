from django.db import models
from django.contrib.auth.models import User
from djangobb_forum import settings as forum_settings
from djangobb_forum.fields import ExtendedImageField
from djangobb_forum.util import smiles, convert_text_to_html

MARKUP_CHOICES = [('bbcode', 'bbcode')]

# Create your models here.
class Topic(models.Model):
    topic = models.CharField(max_length=40)
    topic_icon = ExtendedImageField('Topic Icon', blank=True, default='', upload_to='news/Topic')
    
    def __unicode__(self):
        return self.topic

class NewsItem(models.Model):
    title = models.CharField(max_length=80)
    topic = models.ForeignKey(Topic, verbose_name='Topic')
    published = models.BooleanField()
    submitter = models.ForeignKey(User, related_name='+', verbose_name='Submitter')
    approver = models.ForeignKey(User, related_name='+', verbose_name='Approver', blank=True, null=True)
    submit_time = models.DateTimeField('Created', auto_now_add=True)
    post_time = models.DateTimeField('Posted', blank=True, null=True)
    # The Body Text
    markup = models.CharField('Markup', max_length=15, default=forum_settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    body = models.TextField('Message')
    body_html = models.TextField('HTML version',blank=True)
    
    def __unicode__(self):
        return "{0} ({1})".format(self.title, self.topic.topic)
        
    def save(self, *args, **kwargs):
        self.body_html = convert_text_to_html(self.body, self.markup) 
        self.body_html = smiles(self.body_html)
        super(NewsItem, self).save(*args, **kwargs)
        
    def submitter_username(self):
        return self.submitter.username
        
    def approver_username(self):
        if self.approver is None:
            return "(Unapproved)"
        else: 
            return approver.username
            
    def topic_image(self):
        return self.topic.topic_icon
        
    def topic_name(self):
        return self.topic.topic_name
