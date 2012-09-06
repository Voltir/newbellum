from django import forms
from news.models import NewsItem,Topic

class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ('title','topic','body')
