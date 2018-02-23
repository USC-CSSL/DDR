__author__ = 'joe'

from gensim.models import KeyedVectors as kv
import logging
import time as tm

def load_model(model_path, verbose = True):
    """

    :param model_path: Path to word2vec model
    :param verbose: Boolean. Print logging information while loading model
    :return: word2vec model object, dimensionality of model, unique set of words in model
    """

    if verbose is True:

        datetime = tm.localtime()
        date = '{0:}-{1:}-{2:}'.format(datetime.tm_mon, datetime.tm_mday, datetime.tm_year)
        time = '{0:}:{1:}:{2:}'.format(datetime.tm_hour, datetime.tm_min, datetime.tm_sec)
        
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model = kv.load_word2vec_format(model_path, binary=True)
    num_features = model.vector_size
    model_word_set = set(model.index2word)
    print('Finished loading model')
    return model, num_features, model_word_set
