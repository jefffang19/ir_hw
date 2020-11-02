from django.http import HttpResponse
from ..models import Word
from .utils import get_subset

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_model(request):
    from gensim.models.word2vec import Word2Vec

    if request.method == 'GET':

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

        return HttpResponse("Model created")

    else:
        keyword = request.POST['keyword']

        _, words = get_subset(keyword)
        words = [words]

        # word2vector
        model = Word2Vec(words, size=100, window=5, min_count=2, compute_loss=True, workers=4, sg=1)
        # training_loss = model.get_latest_training_loss()
        # print(training_loss)
        model.save("word2vec_{}_sg.model".format(keyword))

        return HttpResponse("{} Model created".format(keyword))
