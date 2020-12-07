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
        l_index_method = int(request.POST['l_bsbi_spimi'])
        l_sort_by_tf = int(request.POST['l_tf'])
        r_index_method = int(request.POST['r_bsbi_spimi'])
        r_sort_by_tf = int(request.POST['r_tf'])

        docs_set = []
        # bsbi
        if index_method == 0:
            docs_set = PositionInDoc.objects.filter(bsbi__term=origin_keyword)
        # spimi
        elif index_method == 1:
            docs_set = PositionInDoc.objects.filter(spimi__term=origin_keyword)

        # highlight searched word
        search_result = {}
        for i in docs_set:
            appeared_article = Article.objects.get(pk=i.article_id)
            # init a new abstract
            if appeared_article.title not in search_result.keys():
                search_result[appeared_article.title] = {}
                search_result[appeared_article.title]['abstract'] = appeared_article.abstract
                search_result[appeared_article.title]['marker'] = []
                search_result[appeared_article.title]['tf'] = 0

            # save where to draw the marker to abstract
            # [position, <marker> lenght]
            search_result[appeared_article.title]['marker'].append([i.position, len(i.origin_term)])
            search_result[appeared_article.title]['tf'] += 1

        for i in search_result.keys():
            # we draw the marker to abstract in reverse order, so the position won't be screwed up
            search_result[i]['marker'] = sorted(search_result[i]['marker'], key=lambda item: item[0], reverse=True)

            for pos, length in search_result[i]['marker']:
                _abstract = search_result[i]['abstract']
                search_result[i]['abstract'] = _abstract[:pos] + '<mark>' + _abstract[pos:pos + length] + '</mark>' + _abstract[pos + length:]

        # sort by tf
        # sort the dict
        if sort_by_tf == 1:
            search_result = {k: v for k, v in sorted(search_result.items(), key=lambda item: item[1]['tf'], reverse=True)}

        return HttpResponse([search_result])

        return JsonResponse(template_dict, safe=False)

    elif request.method == 'GET':
        return render(request, "search_engine/hw5.html")

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
            search_result[i]['marker'] = sorted(search_result[i]['marker'], key=lambda item: item[0], reverse=True)

            for pos, length in search_result[i]['marker']:
                _abstract = search_result[i]['abstract']
                search_result[i]['abstract'] = _abstract[:pos] + '<mark>' + _abstract[pos:pos + length] + '</mark>' + _abstract[pos + length:]


        return HttpResponse([search_result])

    else:
        return HttpResponse('unsupported method')