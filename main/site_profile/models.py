from django.db import models
from django.contrib.auth.models import User

#Named Profile to allow for request.user.profile
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile')
    pledged = models.BooleanField(default=False)
