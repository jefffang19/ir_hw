from django.db import models

# Create your models here.
class Article(models.Model):
    abstract = models.CharField(max_length=200)

class Word(models.Model):
    context = models.CharField(max_length=200)
    position = models.ManyToManyField(Article)
    pos_in_a_article = models.IntegerField()


    