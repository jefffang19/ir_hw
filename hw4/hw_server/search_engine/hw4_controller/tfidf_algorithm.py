from ..models import Bmc

def tfidf(query_word, method_tf, method_idf):
    # get the docs
    bmc = Bmc.objects.filter(subset = 'colorectal_cancer')
    bmc = list(bmc)

    doc_weight = []

    for i in range(len(bmc)):
        doc_weight.append( [bmc[i].title, tf(query_word, i, method_tf, bmc)*idf(query_word, method_idf, bmc)] )


    return doc_weight

def tf(query_word, doc_n, method, bmc):
    _ftd = ftd(query_word, bmc)
    # raw count
    if method == 0:
        return _ftd[doc_n]['ftd']
    # term frequency
    elif method == 1:
        return _ftd[doc_n]['ftd'] / _ftd[doc_n]['words_cnt']
    # log normalization
    elif method == 2:
        import math
        return math.log(1 + _ftd[doc_n]['ftd'])


def idf(query_word, method, bmc):
    import math
    _nt, _N = nt(query_word, bmc)
    # inverse document frequency
    if method == 0:
        # fix division by zero
        if _nt == 0:
            return 0
        else:
            return math.log(_N/_nt)
    # unary
    elif method == 1:
        return 1
    # inverse document frequency smooth
    elif method == 2:
        return math.log(_N/(_nt+1)) + 1


# definition of ftd and nt, please look at td-idf English Wiki page

def ftd(query_word, bmc):
    articles = [i for i in bmc]

    # Freq(t,d)
    # a array frequncey of query term in each documents
    # element is dictionary
    f_td = []

    for doc in articles:
        temp_ftd = {}
        query_word_cnt = 0
        all_words_cnt = 0
        for paragraph in [doc.background, doc.methods, doc.results, doc.conclusion]:
            for word in paragraph.split(' '):
                all_words_cnt += 1
                if word == query_word:
                    query_word_cnt += 1

        temp_ftd['title'] = doc.title
        temp_ftd['ftd'] = query_word_cnt
        temp_ftd['words_cnt'] = all_words_cnt
        f_td.append(temp_ftd)

    return f_td

# return nt, N
def nt(query_word, bmc):
    articles = [i for i in bmc]

    # query term exist in how many document
    _nt = 0
    # document count
    N = len(articles)

    for doc in articles:
        for paragraph in [doc.background, doc.methods, doc.results, doc.conclusion]:
            for word in paragraph.split(' '):
                if word == query_word:
                    _nt += 1
                    break

    return _nt, N