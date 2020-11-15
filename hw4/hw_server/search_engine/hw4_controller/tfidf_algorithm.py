from ..models import Article

_doc_num = 100

def tfidf(query_word, method):
    _tfidf = []

    for i in range(_doc_num):
        _tfidf.append(tf(query_word, i, method)*idf(query_word, method))

    return _tfidf

def tf(query_word, doc_n, method):
    if method == 0:
        _ftd = ftd(query_word)
        return _ftd[doc_n]['ftd']

def idf(query_word, method):
    import math
    if method == 0:
        _nt, _N = nt(query_word)
        return math.log(_N/_nt)

# definition of ftd and nt, please look at td-idf English Wiki page

def ftd(query_word):
    a = Article.objects.all()
    articles = [i for i in a[:100]]

    # Freq(t,d)
    # a array frequncey of query term in each documents
    # element is dictionary
    f_td = []

    for doc in articles:
        temp_ftd = {}
        query_word_cnt = 0
        all_words_cnt = 0
        for word in doc.abstract.split(' '):
            all_words_cnt += 1
            if word == query_word:
                query_word_cnt += 1

        temp_ftd['title'] = doc.title
        temp_ftd['ftd'] = query_word_cnt
        temp_ftd['words_cnt'] = all_words_cnt
        f_td.append(temp_ftd)

    return f_td

# return nt, N
def nt(query_word):
    a = Article.objects.all()
    articles = [i for i in a[:100]]

    # query term exist in how many document
    _nt = 0
    # document count
    N = len(articles)

    for doc in articles:
        for word in doc.abstract.split(' '):
            if word == query_word:
                _nt += 1
                break

    return _nt, N