from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ..forms import WordForm
from ..models import Article, Bsbi, Spimi, PositionInDoc

import numpy as np  # array handling

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def search(request):
    # user search
    if request.method == 'POST':
        # get search word
        # we do NOT stem in this hw
        origin_keyword = request.POST['keyword']
        # get the bsbi/spimi
        index_method = int(request.POST['bsbi_spimi'])

        l_tfidf = tfidf(origin_keyword, tfidf_method[0], tfidf_method[1], int(request.POST['ldata']))
        l_tfidf.sort(key=lambda x: x[1], reverse=True)
        r_tfidf = tfidf(origin_keyword, tfidf_method[2], tfidf_method[3], int(request.POST['rdata']))
        r_tfidf.sort(key=lambda x: x[1], reverse=True)

        # prepare data for template
        docs_ranking_l = [i[0] for i in l_tfidf]
        docs_weight_l = [i[1] for i in l_tfidf]
        docs_len_l = [i[2] for i in l_tfidf]
        docs_ranking_r = [i[0] for i in r_tfidf]
        docs_weight_r = [i[1] for i in r_tfidf]
        docs_len_r = [i[2] for i in r_tfidf]

        # display formula images
        available_formula = ['images/tf_raw_count.png', 'images/tf_term_frequency.png',
                             'images/tf_log_normalization.png',
                             'images/idf_inverse_document_frequency.png', 'images/idf_unary.png',
                             'images/idf_inverse_document_frequency_smooth.png']

        template_dict = {'l_titles': docs_ranking_l, 'l_weights': docs_weight_l, 'l_len': docs_len_l,
                         'r_titles': docs_ranking_r, 'r_weights': docs_weight_r, 'r_len': docs_len_r,
                         'formula': available_formula, 'lpara': [' ' for i in range(len(docs_ranking_l))], 'rpara': [' ' for i in range(len(docs_ranking_r))]}
        # return render(request, "search_engine/tfidf.html", template_dict)
        return JsonResponse(template_dict, safe=False)

    elif request.method == 'GET':
        # return render(request, "search_engine/tfidf.html", template_dict)

        query_word = 'COVID-19'

        docs_set = PositionInDoc.objects.filter(spimi__term=query_word)

        # highlight searched word
        search_result = {}
        for i in docs_set:
            appeared_article = Article.objects.get(pk = i.article_id)
            # init a new abstract
            if appeared_article.title not in search_result.keys():
                search_result[appeared_article.title] = {}
                search_result[appeared_article.title]['abstract'] = appeared_article.abstract
                search_result[appeared_article.title]['marker'] = []

            # save where to draw the marker to abstract
            # [position, <marker> lenght]
            search_result[appeared_article.title]['marker'].append([i.position, len(i.origin_term)])

        for i in search_result.keys():
            # we draw the marker to abstract in reverse order, so the position won't be screwed up
            sorted(search_result[i]['marker'], key=lambda item: item[0], reverse=True)

            for pos, length in search_result[i]['marker']:
                _abstract = search_result[i]['abstract']
                search_result[i]['abstract'] = _abstract[:pos] + '<mark>' + _abstract[pos:pos + length] + '</mark>' + _abstract[pos + length:]


        return HttpResponse([search_result])

    else:
        return HttpResponse('unsupported method')