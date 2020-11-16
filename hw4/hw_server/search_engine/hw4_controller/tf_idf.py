from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ..models import Article
from ..forms import WordForm

from .tfidf_algorithm import tfidf
import numpy as np  # array handling

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def show_tfidef(request):
    # user search
    if request.method == 'POST':
        # get search word
        # we do NOT stem in this hw
        origin_keyword = request.POST['keyword']
        # get the tfidf method user chose
        tfidf_method = [int(request.POST['ltf']), int(request.POST['lidf']), int(request.POST['rtf']), int(request.POST['ridf'])]

        a = Article.objects.all()

        l_tfidf = tfidf(origin_keyword, tfidf_method[0], tfidf_method[1])
        l_tfidf.sort(key=lambda x: x[1], reverse=True)
        r_tfidf = tfidf(origin_keyword, tfidf_method[2], tfidf_method[3])
        r_tfidf.sort(key=lambda x: x[1], reverse=True)

        # prepare data for template
        docs_ranking_l = [i[0] for i in l_tfidf]
        docs_weight_l = [i[1] for i in l_tfidf]
        docs_ranking_r = [i[0] for i in r_tfidf]
        docs_weight_r = [i[1] for i in r_tfidf]

        # display formula images
        available_formula = ['images/tf_raw_count.png', 'images/tf_term_frequency.png',
                             'images/tf_log_normalization.png',
                             'images/idf_inverse_document_frequency.png', 'images/idf_unary.png',
                             'images/idf_inverse_document_frequency_smooth.png']

        template_dict = {'l_titles': docs_ranking_l, 'l_weights': docs_weight_l,
                         'r_titles': docs_ranking_r, 'r_weights': docs_weight_r,
                         'formula': available_formula}
        # return render(request, "search_engine/tfidf.html", template_dict)
        return JsonResponse(template_dict, safe=False)

    elif request.method == 'GET':
        available_formula = ['images/tf_raw_count.png', 'images/tf_term_frequency.png',
                             'images/tf_log_normalization.png',
                             'images/idf_inverse_document_frequency.png', 'images/idf_unary.png',
                             'images/idf_inverse_document_frequency_smooth.png']

        template_dict = {'formula': available_formula}
        return render(request, "search_engine/tfidf.html", template_dict)

    else:
        return HttpResponse('unsupported method')
