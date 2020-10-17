from django.http import JsonResponse
from django.shortcuts import render
from ..models import Word
from ..forms import WordForm
from search_engine.parsing_utils import string_to_tokens


def zipf_ct(request):
    form = WordForm()

    corrected_keywords = ['mask', 'children', '2003', '2019', 'pneumothorax', 'pneumonia', 'image']

    return_dict = {}

    # query for the data subset
    for ck in corrected_keywords:
        keywords_cleaned = string_to_tokens(ck)
        articles_pk = []  # get the target articles' pk

        w = Word.objects.filter(context=keywords_cleaned[0][0])

        for j in w:
            mode = j.position.get()
            # append article pk
            if mode.pk not in articles_pk:
                articles_pk.append(mode.pk)

        words = {}
        # get the target articles' words
        for i in articles_pk:
            w = Word.objects.filter(position__id=i)
            for j in w:
                if j.context not in words.keys():
                    words[j.context] = 1
                else:
                    words[j.context] += 1

        # sort the dict by value
        words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)}

        # stemming words
        _words = list(words.keys())
        _freq = list(words.values())

        return_dict['{}_words'.format(ck)] = _words
        return_dict['{}_freq'.format(ck)] = _freq
        return_dict['{}_subset_article_num'.format(ck)] = len(articles_pk)

    # return JsonResponse(return_dict)

    return render(request, 'search_engine/chart_ct.html', return_dict)
