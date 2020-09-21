from django.shortcuts import render
from .models import Article, Word
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .forms import WordForm

from search_engine.parsing_utils import data_processor
from search_engine.parsing_utils import string_to_tokens


# Create your views here.
def import_json(request):
    file_path = 'D:\\work\\ir_hw\\hw1\\mydata.json'
    article_words = data_processor(file_path)
    for i in article_words:
        a = Article(abstract = i['sentence'])
        a.save()
        for j in i['words']:
            w = Word(context = j[0], pos_in_a_article = j[1])
            w.save()
            w.position.add(a)

    return JsonResponse({"Import file" : "Json", "Status" : "Success"})

def import_xml(request):
    file_path = 'D:\\work\\ir_hw\\hw1\\test.xml'
    article_word = data_processor(file_path, mode = 'xml')
    a = Article(abstract = article_word['sentence'])
    a.save()
    for j in article_word['words']:
        w = Word(context = j[0], pos_in_a_article = j[1])
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

def get_keywords(request):

    # POST => process the form data from user
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            # parse and clean (stemming..etc) the keywords
            keywords_cleaned = string_to_tokens(form.cleaned_data['keywords'])
            # search keywords in db (Model => Word)
            all_words = []
            for i in keywords_cleaned:
                # retrive all word
                q_set = Word.objects.filter(context=i[0])
                for j in q_set:
                    temp = {}
                    temp['word'] = j.context # keyword name
                    temp['pos'] = j.pos_in_a_article # position in the doc
                    # look up in which docs
                    # get many to many table
                    q_art = j.position.get()

                    # when calculating the which doc, we do ( pk - current_firstpk )
                    q3 = Article.objects.filter()[0]
                    article_firstpk = q3.pk

                    temp['docs'] = q_art.pk - article_firstpk


                    all_words.append(temp)
            
            # now we render the show page
            all_articles = Article.objects.all()

            # make sure which docs has keywords
            # format : [doc1, doc2, doc3] (type int)
            key_docs = []
            for i in all_words:
                if i['docs'] not in key_docs:
                    key_docs.append(i['docs'])

            # make sure where the keywords are in the coresponding doc
            # format : {doc1 : [pos1, pos2], doc2 : [pos3, pos4]}  (type int)
            key_pos = {}
            for i in all_words:
                if i['docs'] not in key_pos.keys():
                    key_pos[i['docs']] = [i['pos'],]
                else:
                    key_pos[i['docs']].append(i['pos'])

            

            words = {'articles' : [i.abstract.split(' ') for i in all_articles] ,'keylines' : key_docs  , 'keywords' : key_pos }
    
            return HttpResponse(loader.get_template('search_engine/show_articles.html').render(words , request))

            # return HttpResponse(all_words)

    # GET => create blank form
    else: 
        form = WordForm()

    return render(request, 'search_engine/search_page.html', {'form' : form})