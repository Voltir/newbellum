from news.models import NewsItem, Topic
from django.contrib import admin
from datetime import datetime

def publish(modeladmin, request, queryset):
    queryset.update(published=True, post_time=datetime.now())
publish.short_description = "Publish News Post"

def unpublish(modeladmin, request, queryset):
    queryset.update(published=False, post_time=None)
    unpublish.short_description = "Unpublish News Post"

class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic_name', 'submitter_username' , 'submit_time', 'post_time', 'published']
    fieldsets = (
        (None, {
            'fields': ('title', 'topic', 'submitter', 'body', 'published'),
         }),
    )
    readonly_fields = ['published']
    ordering = ['submit_time']
    actions = [publish,unpublish]

class TopicAdmin(admin.ModelAdmin):
    pass

admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(Topic, TopicAdmin)