from django.contrib.auth.models import User
from django import forms
from models import Profile 

class RegistrationForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = Profile
        fields = (
            'pledged',
        )
