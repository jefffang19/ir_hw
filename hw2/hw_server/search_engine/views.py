from django.shortcuts import render
from .models import Article, Word, StemFreq, OriginFreq
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .forms import WordForm, UploadFileForm

from search_engine.parsing_utils import data_processor, handle_uploaded_file, count_sent
from search_engine.parsing_utils import string_to_tokens


# Create your views here.
# api function
def import_json(request):
    file_path = 'temp_uploaded'
    article_words = data_processor(file_path, mode = 'json', tag = "tweet_text")
    for i in article_words:
        a = Article(abstract = i['sentence'])
        a.save()
        for j in i['words']:
            w = Word(context = j[0], pos_in_a_article = j[1])
            w.save()
            w.position.add(a)

    # return JsonResponse({"Import file" : "Json", "Status" : "Success"})

    return show_articles(request, True)

# api function
def import_xml(request):
    file_path = 'temp_uploaded'
    many_article = data_processor(file_path, mode = 'xml', tag = 'abstract')

    # debug
    # return HttpResponse(len(many_article))

    for i in many_article:
        a = Article(abstract = i['sentence'])
        a.save()
        for j in i['words']:
            w = Word(context = j[0], pos_in_a_article = j[1])
            w.save()
            w.position.add(a)
        

    # return JsonResponse({"Import file" : "xml", "Status" : "Success"})
    return show_articles(request, True)

# main func
def show_articles(request, first=False):
    # POST => process the form data from user
    # if request.method == 'POST':
    if not first and request.method == 'POST':
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

            len_article = len(all_articles) #count the num of articles

            arts = []
            _str = ""

            # a bug happened because \n
            for i in all_articles:
                for j in i.abstract:
                    if(j != '\n'):
                        _str += j
                    else:
                        _str += ' '
                    
                arts.append(_str)
                _str = ""


            arts = [i.split(' ') for i in arts] # articles break into words
            
            # count sentence num
            tot_sc = 0
            sep_sc = []
            for sc in all_articles:
                tot_sc += count_sent(sc.abstract)
                sep_sc.append(count_sent(sc.abstract))

            # count the num of words
            tot_words = 0
            len_sep_words = []
            
            for wo in arts:
                tot_words += len(wo)
                len_sep_words.append(len(wo))

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

            
            form = WordForm()


            #count

            words = {'form' : form, 'len_article': len_article ,'tot_sc' : tot_sc ,'sep_sc':sep_sc , 'len_words' : tot_words, 'sep_words':len_sep_words, 'articles' :  arts, 'num_result' : len(all_words) , 'keylines' : key_docs  , 'keywords' : key_pos }
            # structure of words
            # {
            #   'articles' : a list of articles to show on template,
            #   'keylines' : a list of which line has words to highlight,
            #   'keywords' : a dict of which word to highlight in the corresponding line,
            #                   key is int , value is list 
            # }

            # debug
            # return JsonResponse({'keylines' : key_docs  , 'keywords' : key_pos})

            return render(request, 'search_engine/show_articles.html', words)
    

    else:
        form = WordForm()
        all_articles = Article.objects.all()

        len_article = len(all_articles) #count the num of articles
        arts = [i.abstract.split(' ') for i in all_articles] # articles break into words
        # count the num of words
        tot_words = 0
        len_sep_words = []

        # count sent num
        tot_sc = 0
        sep_sc = []
        for sc in all_articles:
            tot_sc += count_sent(sc.abstract)
            sep_sc.append(count_sent(sc.abstract))
        
        for wo in arts:
            tot_words += len(wo)
            len_sep_words.append(len(wo))
        words = {'form':form, 'articles' : [i.abstract.split(' ') for i in all_articles] ,'tot_sc' : tot_sc ,'sep_sc':sep_sc , 'len_article' : len_article  , 'len_words' : tot_words, 'sep_words':len_sep_words,}
        
        # return HttpResponse(loader.get_template('search_engine/show_articles.html').render(words , request))
        return render(request, 'search_engine/show_articles.html', words)


# deprecated
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

            

            words = {'articles' : [i.abstract.split(' ') for i in all_articles] , 'num_result' : len(all_words) , 'keylines' : key_docs  , 'keywords' : key_pos }
    
            return HttpResponse(loader.get_template('search_engine/show_articles.html').render(words , request))

            # return HttpResponse(all_words)

    # GET => create blank form
    else:
        form = WordForm()

    return render(request, 'search_engine/search_page.html', {'form' : form})

def upload_file(request):
    if request.method == 'POST':
        del_everything(request)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # store the uploaded file
            handle_uploaded_file(request.FILES['file'])
            if request.POST['mode'] == 'xml':
               return import_xml(request)
            elif request.POST['mode'] == 'json':
                return import_json(request)
            else:
                return HttpResponse('upload success, but wrong mode')
        else:
            return HttpResponse('upload unsuccessful')

    else:
        form = UploadFileForm()

    return render(request, 'search_engine/upload_file_abstract.html', {'form' : form})

def del_everything(request):
    Article.objects.all().delete()
    Word.objects.all().delete()

    return

# hw 2 main template
def zipf(request, opt=0):
    form = WordForm()
    a = 'temp'
    title = 'temp'

    if opt == 0 or opt == 1:
        if opt == 0:
            a = OriginFreq.objects.all()
            title = 'Original'
        elif opt == 1:
            a = StemFreq.objects.all()
            title = 'Stemming'

        top100_words = []
        freq = []
        # other_words = []
        # other_freq = []

        count = 0
        for i in a:
            if count < 100:
                top100_words.append(i.word)
            
            freq.append(i.frequency)
            
            count += 1

        return render(request, 'search_engine/chart.html', {'title' : title, 'form' : form, 'top_words' : top100_words, 'freq' : freq, 'top_words_ori' : [], 'top_words_stem' : [], 'freq_ori' : [], 'freq_stem' : [] })
    elif opt == 2:
        title = 'Both'

        a1 = OriginFreq.objects.all()
        a2 = StemFreq.objects.all()

        top100_words_ori = []
        freq_ori = []
        top100_words_stem = []
        freq_stem = []

        count = 0
        for i in a1:
            if count < 100:
                top100_words_ori.append(i.word)
            
            freq_ori.append(i.frequency)
            
            count += 1

        count = 0
        for i in a2:
            if count < 100:
                top100_words_stem.append(i.word)
            
            freq_stem.append(i.frequency)
            
            count += 1

        return render(request, 'search_engine/chart.html', {'title' : title, 'form' : form, 'top_words_ori' : top100_words_ori, 'top_words_stem' : top100_words_stem, 'freq_ori' : freq_ori, 'freq_stem' : freq_stem, 'top_words' : [], 'freq' : [] })
        

def zipf_search(request, subset = 0):
    # for spelling correction
    from spellchecker import SpellChecker

    spell = SpellChecker()

    form = WordForm()
    corrected_keyword = ''
    search_title = ''

    # user search
    if request.method == 'POST':
        form = WordForm(request.POST)
        # get search word
        if form.is_valid():
            # parse and clean (stemming..etc) the keywords
            origin_keyword = form.cleaned_data['keywords']
            misspelled = spell.unknown([origin_keyword])
            corrected_keyword = ''
            search_title = ''
            
            if len(misspelled)!= 0:
                for w in misspelled:
                    corrected_keyword = spell.correction(w)
                search_title = 'Do you mean \"{}\". Showing search results for {}'.format(corrected_keyword,corrected_keyword)
            else:
                corrected_keyword = origin_keyword
                search_title = 'search results for {}'.format(origin_keyword)

    # predefine subset
    elif subset == 0:
        corrected_keyword = 'mask'
        search_title = 'search results for mask'

    elif subset == 1:
        corrected_keyword = '2005'
        search_title = 'search results for 2005'


    # query for the data subset
    keywords_cleaned = string_to_tokens(corrected_keyword)
    titles = {} # get the target articles names
    articles_pk = [] # get the target articles' pk
    articles_raw_words = {} # get the target articles' abstract raw words

    for i in keywords_cleaned:
        w = Word.objects.filter(context = i[0])

        for j in w:
            mode = j.position.get()
            title = mode.title
            # append article pk
            if mode.pk not in articles_pk:
                articles_pk.append(mode.pk)
                # append raw abstract words
                for k in mode.abstract.split(' '):
                    if k not in articles_raw_words.keys():
                        articles_raw_words[k] = 1
                    else:
                        articles_raw_words[k] += 1
            # append article title
            if title not in titles.keys():
                titles[title] = 1
            else:
                titles[title] += 1

    # sort the dict by value
    titles = {k : v for k, v in sorted(titles.items(), key=lambda  item: item[1], reverse=True)}
    articles_raw_words = {k : v for k, v in sorted(articles_raw_words.items(), key=lambda  item: item[1], reverse=True)}
    titles_name = list(titles.keys())
    titles_freq = list(titles.values())

    words = {}
    # get the target articles' words
    for i in articles_pk:
        w = Word.objects.filter(position__id=i)
        for j in w:
            if j.context not in words.keys():
                words[j.context] = 1
            else:
                words[j.context] += 1
    
    # sort the dict by value
    words = {k : v for k, v in sorted(words.items(), key=lambda  item: item[1], reverse=True)}

    # calculate zipf
    # of = OriginFreq.objects.filter(word == )
    # sf = StemFreq.objects.all()
    title = str(corrected_keyword)

    top100_words = list(words.keys())[:100]
    freq = list(words.values())

    top100_words_raw = list(articles_raw_words.keys())[:100]
    freq_raw = list(articles_raw_words.values())
    
    return render(request, 'search_engine/chart_search.html', {'search_title':search_title, 'titles_name' : titles_name, 'titles_freq': titles_freq, 'chart_title' : title, 'form' : form, 'top_words' : top100_words, 'freq' : freq, 'top_words_raw' : top100_words_raw, 'freq_raw' : freq_raw })



def search_covid(request):
    w = Word.objects.filter(context = "covid19")

    titles = {}
    for i in w:
        title = i.position.get().title
        if title not in titles.keys():
            titles[title] = 1
        else:
            titles[title] += 1

    # sort the dict by value
    titles = {k : v for k, v in sorted(titles.items(), key=lambda  item: item[1], reverse=True)}
    
    return JsonResponse(titles)

# an api to import pubmed xml
def import_pubmed(request):
    import pandas as pd
    # read the 10000 files from csv
    num_of_csv = 1000
    count = 0
    no10 = []
    for i in range(1,num_of_csv+1):
        dataframe = pd.read_csv('pubmed/{}.csv'.format(i))
        count += dataframe.shape[0]
        if dataframe.shape[0] != 10:
            no10.append(i)
        titles = list(dataframe['title'])
        abstracts = list(dataframe['abstract'])
        for j in range(len(titles)):
            a = Article(title = titles[j], abstract = abstracts[j])
            a.save()

    return HttpResponse('import success{}'.format(count))
    # return JsonResponse({'problem csv' : no10})

# an api to create reverse index
def create_revindex(request):
    a = Article.objects.all()
    word_freq = {}
    for i in a:
        for j in string_to_tokens(i.abstract):
            if j[0] != 'nan':
                w = Word(context = j[0], pos_in_a_article = j[1])
                w.save()
                w.position.add(i)
    
    return HttpResponse('Create Reverse index success')

# create origin word frequency table
def create_origin_freq(request):
    a = Article.objects.all()
    m = {}
    # calculate the freq of each word
    for i in a:
        for j in i.abstract.split(' '):
            if j in m.keys():
                m[j] += 1
            else:
                m[j] = 1

    # sort the dict by value
    m = {k : v for k, v in sorted(m.items(), key=lambda  item: item[1], reverse=True)}

    # save to database
    for j in m.keys():
        of = OriginFreq(word = j, frequency = m[j])
        of.save() 

    return HttpResponse('OriginFreq created')

# create stem word frequency table
def create_stem_freq(request):
    a = Article.objects.all()
    word_freq = {}
    for i in a:
        for j in string_to_tokens(i.abstract):
            if j[0] != 'nan':
                if j[0] in word_freq.keys():
                    word_freq[j[0]] += 1
                else:
                    word_freq[j[0]] = 0
                    
    # sort the dict by value
    word_freq = {k : v for k, v in sorted(word_freq.items(), key=lambda  item: item[1], reverse=True)}

    #save to database
    for j in word_freq.keys():
        sf = StemFreq(word = j, frequency = word_freq[j])
        sf.save() 

    return HttpResponse('StemFreq created')
