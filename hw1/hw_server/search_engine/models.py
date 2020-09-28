from django.db import models

# Create your models here.
class Article(models.Model):
    abstract = models.CharField(max_length=200)
    label = models.CharField(max_length=200, default=None, blank=True, null=True)
    articleId = models.IntegerField(default=None, blank=True, null=True)

class Word(models.Model):
    context = models.CharField(max_length=200)
    position = models.ManyToManyField(Article)
    pos_in_a_article = models.IntegerField()


    