from __future__ import division

import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import collections
import logging
from gensim.models import Word2Vec
import csv
import time as tm
import file_length
import pandas as pd
from simple_progress_bar import update_progress
from get_vecs import make_agg_vec


datetime = tm.localtime()
date = '{0:}-{1:}-{2:}'.format(datetime.tm_mon, datetime.tm_mday, datetime.tm_year)
time = '{0:}:{1:}:{2:}'.format(datetime.tm_hour, datetime.tm_min, datetime.tm_sec)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_model(model_path):
    """Load Word2Vec model and return model, number of features, and word index"""


    model = Word2Vec.load_word2vec_format(model_path, binary=True)
    num_features = model.layer1_size
    model_word_set = set(model.index2word)
    print 'Finished loading model'
    return model, num_features, model_word_set


def get_loadings(agg_doc_vecs_path, agg_dic_vecs_path, out_path, num_features, delimiter='\t'):
    """Get loadings between each document vector in agg-doc_vecs_path and each dictionary dimension in
    agg_dic_vecs_path"""


    n_docs = float(file_length.file_len(agg_doc_vecs_path))
    prog_counter = 0
    counter = 0
    dic_vecs = pd.read_csv(agg_dic_vecs_path, sep=delimiter)
    dic_vecs = dic_vecs.to_dict(orient='list')

    with open(agg_doc_vecs_path, 'rb') as doc_vecs, open(out_path, 'wb') as out_file:

        doc_vecs_reader = csv.reader(doc_vecs, delimiter='\t')
        doc_vecs_reader.next()

        writer = csv.writer(out_file, delimiter='\t')
        fieldnames_out = ['ID'] + dic_vecs.keys()

        writer.writerow(fieldnames_out)

        for doc_vec in doc_vecs_reader:

            prog_counter += 1
            counter += 1
            doc_id = doc_vec[0]
            out_row = [doc_id]

            for dic_vec in dic_vecs.keys():
                doc_vec = [float(x) for x in doc_vec[-num_features:]]
                dic_similarity = cosine_similarity(doc_vec, dic_vecs[dic_vec])[0][0]
                out_row.append(dic_similarity)

            writer.writerow(out_row)

            if prog_counter >= 0.05 * n_docs:
                prog_counter = 0
                update_progress(counter / (n_docs - 1))

        print 'Finished calculating document loadings'

