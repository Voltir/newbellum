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
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        newsitem = NewsItem.objects.get(pk=object_id)
        extra_context['newsitem'] = newsitem
        return super(NewsItemAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)
        

class TopicAdmin(admin.ModelAdmin):
    pass

admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(Topic, TopicAdmin)