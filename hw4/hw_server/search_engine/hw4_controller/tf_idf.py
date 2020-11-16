from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ..models import Article
from ..forms import WordForm

from .tfidf_algorithm import tfidf
import numpy as np  # array handling

from django.views.decorators.csrf import csrf_exempt


def show_tfidef(request):
    # user search
    if request.method == 'POST':
        form = WordForm(request.POST)
        # get search word
        if form.is_valid():
            # we do NOT stem in this hw
            origin_keyword = form.cleaned_data['keywords']

            a = Article.objects.all()

            _tfidf = tfidf(origin_keyword, 0, 1)
            _tfidf.sort(key=lambda x: x[1], reverse=True)

            # prepare data for template
            docs_ranking = [i[0] for i in _tfidf]
            docs_weight = [i[1] for i in _tfidf]

            template_dict = {'form': form, 'l_titles': docs_ranking, 'l_weights': docs_weight,
                             'r_titles': docs_ranking, 'r_weights': docs_weight}
            return render(request, "search_engine/tfidf.html", template_dict)

        else:
            return HttpResponse('keyword serach failed')

    elif request.method == 'GET':
        form = WordForm()

        display_formula = ['images/tf_raw_count.png', 'images/idf_unary.png', 'images/tf_term_frequency.png', 'images/idf_inverse_document_frequency.png']

        template_dict = {'form': form, 'formula': display_formula}
        return render(request, "search_engine/tfidf.html", template_dict)

    else:
        return HttpResponse('unsupported method')
