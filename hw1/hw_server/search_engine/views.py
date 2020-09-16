from django.shortcuts import render
from .models import Article, Word
from django.http import HttpResponse, JsonResponse
from django.template import loader

from search_engine.parsing_utils import data_processor


# Create your views here.
def import_json(request):
    file_path = 'D:\\work\\ir_hw\\hw1\\mydata.json'
    article_words = data_processor(file_path)
    for i in article_words:
        a = Article(abstract = i['sentence'])
        a.save()
        for j in i['words']:
            w = Word(context = j)
            w.save()
            w.position.add(a)

    return JsonResponse({"Import file" : "Json", "Status" : "Success"})

def show_articles(request):
    all_articles = Article.objects.all()
    
    return HttpResponse(loader.get_template('search_engine/show_articles.html').render({ 'articles' : [i.abstract for i in all_articles]} , request))
