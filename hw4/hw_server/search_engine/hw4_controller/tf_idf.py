from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ..models import Article
from ..forms import WordForm

from .tfidf_algorithm import tfidf
import numpy as np  # array handling

from django.views.decorators.csrf import csrf_exempt

def show_tfidef(request):
    a = Article.objects.all()

    _tfidf = tfidf('COVID-19', 1, 1)
    _tfidf.sort(key=lambda x: x[1], reverse=True)
    # return HttpResponse([_tfidf])

    form = WordForm()

    template_dict = {'form' : form}
    return render(request, "search_engine/tfidf.html", template_dict)