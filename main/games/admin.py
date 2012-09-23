'''
Created on Sep 16, 2012

@author: Rex
'''
from django.contrib import admin
from games.models   import Game, GameMember

class GameAdmin(admin.ModelAdmin):
    list_display = ['image_display', 'title']
    exclude = ['long_desc_html']

class GameMemberAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Game, GameAdmin)
admin.site.register(GameMember, GameMemberAdmin)
