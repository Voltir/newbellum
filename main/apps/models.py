from django.db import models

# Create your models here.
class App(models.Model):
    title = models.CharField(max_length=80)

class Question(models.Model):
    application = models.ForeignKey(App, verbose_name="Application", blank = True, null = True)
    