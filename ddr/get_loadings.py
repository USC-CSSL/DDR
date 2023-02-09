from __future__ import division

import numpy as np
import logging
import csv
import time as tm
import file_length
import pandas as pd
from simple_progress_bar import update_progress

from cosine_similarity import cos_similarity


datetime = tm.localtime()
date = '{0:}-{1:}-{2:}'.format(datetime.tm_mon, datetime.tm_mday, datetime.tm_year)
time = '{0:}:{1:}:{2:}'.format(datetime.tm_hour, datetime.tm_min, datetime.tm_sec)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_loadings(agg_doc_vecs_path, agg_dic_vecs_path, out_path, num_features, delimiter='\t'):
    '''

    :param agg_doc_vecs_path: Path to distributed representations of documents
    :param agg_dic_vecs_path: Path to distributed representations of dictionaries
    :param out_path: Path to write to
    :param num_features: Number of dimensions in distributed representations
    :param delimiter: Delimiter to use
    :return:
    '''
    """Get loadings between each document vector in agg-doc_vecs_path and each dictionary dimension in
    agg_dic_vecs_path"""
    n_docs = float(file_length.file_len(agg_doc_vecs_path))
    prog_counter = 0
    counter = 0
    dic_vecs = pd.read_csv(agg_dic_vecs_path, sep=delimiter)
    dic_vecs = dic_vecs.to_dict(orient='list')
    nan_counter = {'ID': [], 'count': 0}

    with open(agg_doc_vecs_path, 'rb') as doc_vecs, open(out_path, 'wb') as out_file:

        doc_vecs_reader = csv.reader(doc_vecs, delimiter=delimiter)
        doc_vecs_reader.next()

        writer = csv.writer(out_file, delimiter=delimiter)
        fieldnames_out = ['ID'] + list(dic_vecs.keys())

        writer.writerow(fieldnames_out)

        for doc_vec in doc_vecs_reader:

            if 'nan' in doc_vec:
                nan_counter['count'] += 1
                nan_counter['ID'].append(doc_vec[0])
                pass

            else:
                prog_counter += 1
                counter += 1
                doc_id = doc_vec[0]
                out_row = [doc_id]

                for k in dic_vecs.iterkeys():


                    doc_vec = [np.float64(x) for x in doc_vec[-num_features:]]

                    dic_similarity = cos_similarity(doc_vec, dic_vecs[k])
                    out_row.append(dic_similarity)

                writer.writerow(out_row)
                if prog_counter >= 0.01 * n_docs:
                    prog_counter = 0
                    update_progress(counter / (n_docs - 1))

        print('Failed to calculate {0} loadings due to missing values.'.format(nan_counter['count']))
        print('IDs for documents with missing values:\n\n', nan_counter['ID'])
