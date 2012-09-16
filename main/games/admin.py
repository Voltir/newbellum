'''
Created on Sep 16, 2012

@author: Rex
'''
from django.contrib import admin
from games.models   import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ['image_display', 'title']
    exclude = ['long_desc_html']
    
admin.site.register(Game, GameAdmin)
