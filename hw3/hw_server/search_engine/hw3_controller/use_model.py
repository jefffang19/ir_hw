from django.http import HttpResponse
from django.shortcuts import render
from ..models import Word, StemFreq, Tsne

import pandas as pd

from sklearn.decomposition import IncrementalPCA    # inital reduction
from sklearn.manifold import TSNE                   # final reduction
import numpy as np                                  # array handling


def use_model(request):
    from gensim.models.word2vec import Word2Vec

    model = Word2Vec.load("word2vec_sg.model")
    most_similar(model, ['china', 'mask', 'ct'], 100).to_csv("word2vec.csv")

    # find top 100 high freq word in covid19 set
    sf = StemFreq.objects.all()[:100]
    top_words = []
    for i, w in enumerate(sf):
        # if i >= 100:
        #     break
        top_words.append(w.word)

    # get all label and (x,y)
    tsne = Tsne.objects.filter(model_num = 0)

    x_vals = []
    y_vals = []
    labels = []
    for i in tsne:
        x_vals.append(i.x_val)
        y_vals.append(i.y_val)
        labels.append(i.label)

    # plot_with_matplotlib(x_vals, y_vals, labels, top_words)

    return_dict = {
        'high_x' : x_vals[:1000],
        'high_y' : y_vals[:1000],
        'mid_x' : x_vals[1000:10000],
        'mid_y' : y_vals[1000:10000],
        'low_x' : x_vals[10000:],
        'low_y' : y_vals[10000:],
    }

    return render(request, 'search_engine/w2v_tsne.html', return_dict)

# tsne reduce dim cost a lot of time
def tsne(request):
    from gensim.models.word2vec import Word2Vec

    model = Word2Vec.load("word2vec_sg.model")
    x_vals, y_vals, labels = reduce_dimensions(model)

    # count model #
    model_num = 0
    ts = Tsne.objects.all()

    if len(ts) != 0:
        model_num = ts[-1].model_num + 1

    for i in range(len(labels)):
        Tsne.objects.create(model_num = model_num, x_val = x_vals[i], y_val = y_vals[i], label = labels[i], dataset_name = "Covid-19")

    return HttpResponse("tsne data create success")


def most_similar(w2v_model, words, topn=10):
    similar_df = pd.DataFrame()
    for word in words:
        try:
            similar_words = pd.DataFrame(w2v_model.wv.most_similar(word, topn=topn), columns=[word, 'cos'])
            similar_df = pd.concat([similar_df, similar_words], axis=1)
        except:
            print(word, "not found in Word2Vec model!")
    return similar_df


def reduce_dimensions(model):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)

    vectors = [] # positions in vector space
    labels = [] # keep track of words to label our data again later
    for word in model.wv.vocab:
        vectors.append(model.wv[word])
        labels.append(word)

    # convert both lists into numpy vectors for reduction
    vectors = np.asarray(vectors)
    labels = np.asarray(labels)

    # reduce using t-SNE
    vectors = np.asarray(vectors)
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]

    print(x_vals[:5])
    return x_vals, y_vals, labels


def plot_with_matplotlib(x_vals, y_vals, labels, draw_words):
    import matplotlib.pyplot as plt
    import random

    random.seed(0)

    plt.figure(figsize=(12, 12))
    plt.scatter(x_vals, y_vals)

    #
    # Label draw_words[]
    #
    selected_indices = []
    for i in range(len(labels)):
        if labels[i] in draw_words:
            selected_indices.append(i)

    for i in selected_indices:
        plt.annotate(labels[i], (x_vals[i], y_vals[i]))

    plt.savefig('model_fig.png')
