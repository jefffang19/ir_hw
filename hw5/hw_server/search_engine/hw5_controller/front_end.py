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
        # get the tfidf method user chose
        tfidf_method = [int(request.POST['ltf']), int(request.POST['lidf']), int(request.POST['rtf']), int(request.POST['ridf'])]

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
        # available_formula = ['images/tf_raw_count.png', 'images/tf_term_frequency.png',
        #                      'images/tf_log_normalization.png',
        #                      'images/idf_inverse_document_frequency.png', 'images/idf_unary.png',
        #                      'images/idf_inverse_document_frequency_smooth.png']
        #
        # template_dict = {'formula': available_formula}
        # return render(request, "search_engine/tfidf.html", template_dict)

        query_word = 'COVID-19'

        # articles_set = Article.objects.all()

        docs_set = PositionInDoc.objects.filter(spimi__term=query_word)

        # high light searched word
        search_result = {}
        for i in docs_set:
            appeared_article = Article.objects.get(pk = i.article_id)
            if appeared_article.title not in search_result.keys():
                search_result[appeared_article.title] = {}
                search_result[appeared_article.title]['abstract'] = appeared_article.abstract

            _abstract = search_result[appeared_article.title]['abstract']
            search_result[appeared_article.title]['abstract'] = _abstract[:i.position] + '<mark>' + _abstract[i.position:i.position + len(i.origin_term)] + '</mark>' + _abstract[i.position + len(i.origin_term):]


        return HttpResponse([search_result])

    else:
        return HttpResponse('unsupported method')