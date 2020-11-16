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
        print(origin_keyword)

        a = Article.objects.all()

        _tfidf = tfidf(origin_keyword, 0, 1)
        _tfidf.sort(key=lambda x: x[1], reverse=True)

        # prepare data for template
        docs_ranking = [i[0] for i in _tfidf]
        docs_weight = [i[1] for i in _tfidf]

        # display formula images
        available_formula = ['images/tf_raw_count.png', 'images/tf_term_frequency.png',
                             'images/tf_log_normalization.png',
                             'images/idf_inverse_document_frequency.png', 'images/idf_unary.png',
                             'images/idf_inverse_document_frequency_smooth.png']

        template_dict = {'l_titles': docs_ranking, 'l_weights': docs_weight,
                         'r_titles': docs_ranking, 'r_weights': docs_weight,
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
