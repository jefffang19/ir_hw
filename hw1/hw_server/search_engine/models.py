from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.CharField(max_length=200)

class Word(models.Model):
    context = models.CharField(max_length=200)
    position = models.ManyToManyField(Article)
    