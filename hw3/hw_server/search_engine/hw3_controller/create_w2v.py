from django.http import HttpResponse
from django.shortcuts import render
from ..models import Word, StemFreq

import pandas as pd

from sklearn.decomposition import IncrementalPCA    # inital reduction
from sklearn.manifold import TSNE                   # final reduction
import numpy as np                                  # array handling

def create_model(request):
    from gensim.models.word2vec import Word2Vec

    w = Word.objects.all()

    words = []

    for i in w:
        # check if is English words
        if i.context.isascii():
            words.append(i.context)

    words = [words]

    # word2vector
    model = Word2Vec(words, size=100, window=5, min_count=2, compute_loss=True, workers=4, sg=1)
    # training_loss = model.get_latest_training_loss()
    # print(training_loss)
    model.save("word2vec_sg.model")

    most_similar(model, ['china', 'mask', 'ct'], 100).to_csv("word2vec.csv")

    # find top 100 high freq word in covid19 set
    sf = StemFreq.objects.all()
    top_words = []
    for i,w in enumerate(sf):
        if i >= 100:
            break
        top_words.append(w.word)

    x_vals, y_vals, labels = reduce_dimensions(model)
    plot_with_matplotlib(x_vals, y_vals, labels, top_words)

    return HttpResponse()
    # return HttpResponse("{}".format(most_similar(model, ['china'])))

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
