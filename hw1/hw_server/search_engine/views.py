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

def import_xml(request):
    file_path = 'D:\\work\\ir_hw\\hw1\\test.xml'
    article_word = data_processor(file_path, mode = 'xml')
    a = Article(abstract = article_word['sentence'])
    a.save()
    for j in article_word['words']:
        w = Word(context = j)
        w.save()
        w.position.add(a)

    return JsonResponse({"Import file" : "xml", "Status" : "Success"})

def show_articles(request):
    all_articles = Article.objects.all()
    # structure of words
    # {
    #   'articles' : a list of articles to show on template,
    #   'keylines' : a list of which line has words to highlight,
    #   'keywords' : a dict of which word to highlight in the corresponding line,
    #                   key is int , value is list 
    # }
    words = {'articles' : [i.abstract.split(' ') for i in all_articles] ,'keylines' : [1,2]  , 'keywords' : {1:[2, 4] ,2:[4]}}
    
    return HttpResponse(loader.get_template('search_engine/show_articles.html').render(words , request))
