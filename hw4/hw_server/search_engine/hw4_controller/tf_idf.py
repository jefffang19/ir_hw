from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ..models import Article

from .tfidf_algorithm import tfidf
import numpy as np  # array handling

from django.views.decorators.csrf import csrf_exempt

def show_tfidef(request):
    a = Article.objects.all()

    _tfidf = tfidf('COVID-19', 0)
    return HttpResponse([_tfidf])