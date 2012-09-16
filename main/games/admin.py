'''
Created on Sep 16, 2012

@author: Rex
'''
from django.contrib import admin
from games.models   import Game

class GameAdmin(admin.ModelAdmin):
    exclude = ['long_desc_html']
    
admin.site.register(Game, GameAdmin)
