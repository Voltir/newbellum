from django.db import models
from djangobb_forum.fields import ExtendedImageField
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from apps.models import App
from postmarkup import render_bbcode
from djangobb_forum.util import smiles
from django.conf import settings

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=80)
    short_desc = models.CharField(max_length=200, verbose_name = 'Short Description')
    long_desc = models.TextField('Long Description')
    long_desc_html = models.TextField('Long Description')
    image = ExtendedImageField('Game Image', blank=True, default='', upload_to='games/Image')
    server = models.CharField(max_length=80)
    server_url = models.URLField(verbose_name='Server Information URL', blank=True, null=True)
    faction = models.CharField(max_length=80)
    faction_url = models.URLField(verbose_name='Faction Information URL', blank=True, null=True)
    game_info_url = models.URLField(verbose_name='Game Info URL', blank=True, null=True)
    require_app = models.BooleanField(verbose_name='Require Application')
    app = models.ForeignKey(App, verbose_name='Application', blank=True, null=True)
    members_group = models.ForeignKey(Group, verbose_name='Members Group', blank=True, null=True)
    active = models.BooleanField(verbose_name='Require Application', default=False)
    game_members = models.ManyToManyField(User, through='GameMember')
    
    def save(self, *args, **kwargs):
        '''Render the long description into HTML on save'''
        
        self.long_desc_html = render_bbcode(self.long_desc) 
        self.long_desc_html = smiles(self.long_desc_html)
        super(Game, self).save(*args, **kwargs)
        
    def get_membership(self, user):
        try:
            return GameMember.objects.get(user=user, game=self)
        except:
            return None
    
    def view_detail_url(self):
        return reverse('game_detail_view',args=[self.pk])
    
    def image_display(self):
        filename = settings.MEDIA_URL + str(self.image)
        return '<img src="{0}" />'.format(filename)
    image_display.allow_tags = True
    
class GameMember(models.Model):
    game = models.ForeignKey(Game, verbose_name="Member of Game")
    user = models.ForeignKey(User)
    date = models.DateField("Date Joined", None, auto_now=True, auto_now_add=True)
    
    