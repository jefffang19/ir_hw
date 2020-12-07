from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ..forms import WordForm
from ..models import Article, BsbiBlocks, PositionInDoc, Bsbi

from .utils import find_all, parse_mesh_func

import numpy as np  # array handling

from django.views.decorators.csrf import csrf_exempt

def parse_mesh(request):
    mesh = open('../c2020.bin')

    # deal with the first line
    line = mesh.readline()

    # word : [Synonyms]
    index = {}

    # Synonym : word
    inverted_index = {}

    _index = ''
    while line:
        line = mesh.readline()
        if line == '*NEWRECORD\n':
            _index = ''
        elif line[:2] == 'NM' and line[:5] != 'NM_TH':
            # print(line, end='')
            _index = line[5:-1].split(',')[0]
            #         print(_index)

            # create a synonyms index
            index[_index] = []

        elif line[:2] == 'SY':
            # print(line, end='')

            # append to synonyms index
            index[_index].append(line[5:].split('|')[0])
            # create a inverted index
            inverted_index[line[5:].split('|')[0]] = _index

    # filter out words without covid19
    filt_index = {}
    for i in index.keys():
        if ('COVID' in i) or ('covid' in i):
            filt_index[i] = index[i]


    # return JsonResponse(inverted_index)
    # return HttpResponse(len(inverted_index))
    # return HttpResponse([index.values()])
    return JsonResponse(filt_index)

def bsbi(request):
    articles_set = Article.objects.all()
    # articles = []
    #
    # # get all article
    # for i in articles_set:
    #     articles.append(i.abstract)

    # get mesh dictionary (covid-19 related)
    mesh, mesh_inv = parse_mesh_func()

    bsbi_dict = {}

    # count time
    import time

    start_time = time.time()

    # find mesh term
    for cnt, art in enumerate(articles_set):
        # print(cnt)
        for mesh_term in mesh_inv.keys():
            # print(art)
            pos = list(find_all(art.abstract, mesh_term))

            if mesh_inv[mesh_term] not in bsbi_dict:
                bsbi_dict[mesh_inv[mesh_term]] = []

            # mesh term exist
            if len(pos) != 0:
                posins = []
                posins_db = []
                for p in pos:
                    # make dictionary
                    pos_dict = {}
                    pos_dict['article_id'] = art.pk
                    pos_dict['position'] = p
                    pos_dict['origin_term'] = mesh_term
                    posins.append(pos_dict)

                    # write to db
                    posin = PositionInDoc(article_id = art.pk, position = p, origin_term = mesh_term)
                    posin.save()
                    posins_db.append(posin)

                # write to db
                b = BsbiBlocks(term = mesh_inv[mesh_term])
                b.save()
                b.position.add(art)
                for _cnt, j in enumerate(posins):
                    # add to dictionary
                    bsbi_dict[mesh_inv[mesh_term]].append(j)
                    # add to db
                    b.pos_in_a_article.add(posins_db[_cnt])

    # sort the dict by value
    bsbi_dict = {k: v for k, v in sorted(bsbi_dict.items(), key=lambda item: item[0], reverse=True)}

    for term in bsbi_dict.keys():
        print(term)
        _term_list = bsbi_dict[term]
        _posins = []
        for i in _term_list:
            posin = PositionInDoc(article_id=i['article_id'], position=i['position'], origin_term=i['origin_term'])
            posin.save()
            _posins.append(posin)

        # save merge block to db
        b = Bsbi(term=term)
        b.save()
        for i in _posins:
            b.pos_in_a_artcle.add(i)

    end_time = time.time()


    # return JsonResponse(bsbi_dict)
    return JsonResponse({'time cost of bsbi(sec):' : end_time - start_time})

    # return HttpResponse([sorted(list(bsbi_dict.keys()))])
    # return HttpResponse([list(bsbi_dict.keys())])

def bsbi_spimi_time(request):
    return JsonResponse({"time cost of bsbi(sec):": 133.5524184703827})