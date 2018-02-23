from __future__ import division

__author__ = 'Joe Hoover'

import sys
import numpy as np
from load_terms import get_files
import os
import collections
import csv
from file_length import file_len
import pandas as pd
from simple_progress_bar import update_progress


def make_agg_vec(words, model, num_features, model_word_set, filter_out=[]):
    """Create aggregate representation of list of words"""

    feature_vec = np.zeros((num_features,), dtype="float32")

    nwords = 0.

    for word in words:
        if word not in filter_out:
            if word in model_word_set:
                nwords += 1
                feature_vec = np.add(feature_vec, model[word])

    avg_feature_vec = feature_vec / nwords

    return avg_feature_vec


def dic_vecs(dic_terms, model, num_features, model_word_set, filter_out=[]):
    '''

    :param dic_terms: Dictionary where keys are dimension names and values are terms.
    :param model: word2vec model
    :param num_features: Number of dimensions in word2vec model
    :param model_word_set: Set of unique words in word2vec model
    :param filter_out: Words to exclude from aggregation
    :return: A dictionary where keys are dimension names and values the latent semantic space
     representing that dimension. len(values) will equal num_features.
    '''
    agg_dic_vecs = collections.OrderedDict()
    for k in dic_terms.iterkeys():
        agg_dic_vecs[k] = make_agg_vec(dic_terms[k], model = model, num_features = num_features,
                                         model_word_set = model_word_set, filter_out = filter_out)

    return agg_dic_vecs

def write_dic_vecs(dic_vecs, output_path, delimiter='\t'):
    '''

    :param dic_vecs: Dictionary of term dictionary representations (e.g. as created by dic_vecs()
    :param output_path: File to write to
    :param delimiter: Delimiter for column sep in output file
    :return: None
    '''
    dic_vecs = pd.DataFrame.from_dict(dic_vecs, orient='columns')
    dic_vecs.to_csv(output_path, sep=delimiter, index=False)


def doc_vecs_from_csv(input_path, output_path, model, num_features, model_word_set, text_col, delimiter, filter_out=[],
                  quotechar=None,
                  id_col=False, header=True):
    """
    Create a distributed representation of each document in a column of documents
    contained in the input file. These representations are written to the file
    specified by the 'output_path' parameter.

    :param input_path: Path to csv containing text to be represented
    :param output_path: Path to file where results should be written
    :param model: word2vec model to use for representation
    :param num_features: Number of dimensions in word2vec model
    :param model_word_set: Set of unique words in word2vec model
    :param text_col: Column containing text to be represented. This can either be a column name or an
    integer representing the column position. Note that column indices begin at 0.
    :param filter_out: Words to exclude from representations
    :param delimiter: Delimiter used to separate columns in the input file
    :param quotechar: If quote character is used to indicate text in the input file,
    specify what character is used.
    :param id_col: If an ID column is included in the input file, specify
    the column it is located in via column name or position. If no ID column is available,
     this should be set to False. When id_col==False, a sequence of range(1:len(text_col))
     will be generated and each representation will be
    associated with a unique integer that corresponds to the row order in the original file.
    :param header: boolean indicating whether the input file contains a header (True) or not (False).
    :return: None. This function iteratively writes each document representation to file, no
    object is returned.
    """

    with open(input_path, 'rb') as docs_file, open(output_path, 'wb') as out_file:

        docs = csv.reader(docs_file, delimiter=delimiter, quotechar=quotechar)

        if header is True:
            header = docs.next()
            print(header)

            if id_col is not False:
                try:
                    id_col = header.index(id_col)
                except ValueError:
                    try:
                        id_col = int(id_col)
                    except ValueError:
                        print("ValueError: Column '{0}' not found, please make sure that the name or index was correctly listed".format(id_col))

            try:
                print(text_col)
                text_col = header.index(text_col)
            except ValueError:
                try:
                    text_col = int(text_col)
                except ValueError:
                    print("ValueError: Column '{0}' not found, please make sure that the name or index was correctly listed".format(text_col))

        if header is False:
            if id_col is not False:
                try:
                    id_col = int(id_col)
                except ValueError:
                    print("ValueError: Column '{0}' not found, please make sure that the index was correctly listed".format(id_col))

            try:
                text_col = int(text_col)
            except ValueError:
                print("ValueError: Column '{0}' not found, please make sure that the index was correctly listed".format(text_col))

        fieldnames = ['ID'] + [unicode(fnum) for fnum in range(1, num_features + 1)]
        writer = csv.writer(out_file, delimiter=delimiter, quotechar=quotechar)
        writer.writerow(fieldnames)

        n_lines = float(file_len(input_path))
        print(n_lines)
        n_na = 0

        print('Generating aggregate distributed representations of', n_lines, 'texts.')
        update_progress(0 / (n_lines - 1))

        prog_counter = 0
        counter = 0

        if id_col is False:
            cur_id = 0

            for row in docs:
                try:
                    cur_id += 1
                    prog_counter += 1
                    counter += 1

                    doc = row[text_col].split()
                    cur_agg_vec = make_agg_vec(words=doc, model=model, num_features=num_features, model_word_set=model_word_set, filter_out=[])
                    writer.writerow([cur_id] + list(cur_agg_vec))

                    if prog_counter >= 0.05 * n_lines:
                        prog_counter = 0
                        update_progress(counter / (n_lines - 1))

                except IndexError:
                    n_na += 1
                    pass

        elif id_col is not False:
            for row in docs:
                prog_counter += 1
                counter += 1
                
                doc = row[text_col].split()
                cur_agg_vec = make_agg_vec(words=doc, model=model, num_features=num_features, model_word_set=model_word_set, filter_out = [])

                writer.writerow([row[id_col]] + list(cur_agg_vec))

                if prog_counter >= 0.05 * n_lines:
                    prog_counter = 0
                    update_progress(counter / (n_lines - 1))

            print("\nFinished calculating aggregate document representations", "\nNumber NA:", n_na)



def doc_vecs_from_txt(input_path, output_path, num_features, model, model_word_set, delimiter='\t', filter_out = []):
    '''

    :param input_path: Path to text file(s) containing texts to be represented.
    This can be a single file or a directory containing multiple files.
    :param output_path:  Path to file where results should be written
    :param num_features: Number of dimensions in word2vec model
    :param model: word2vec model to use for representation
    :param model_word_set: Set of unique words in word2vec model
    :param filter_out: words to be excluded from the representation from
    :return: None. None. This function iteratively writes each document representation to file, no
    object is returned.
    '''

    path_info = get_files(input_path=input_path)

    with open(output_path, 'wb') as out_file:

        fieldnames = ['ID'] + [unicode(fnum) for fnum in range(1, num_features + 1)]
        writer = csv.writer(out_file, delimiter=delimiter)
        writer.writerow(fieldnames)

        for input_path in path_info.itervalues():

            with open(input_path, 'rb') as docs:

                n_lines = float(file_len(input_path))

                print('Generating aggregate distributed representations of', n_lines, 'texts.')
                update_progress(0 / (n_lines - 1))

                prog_counter = 0
                counter = 0

                cur_id = 0
                n_na = 0

                for row in docs:

                    try:
                        cur_id += 1
                        prog_counter += 1
                        counter += 1
                        row = row[0].split()
                        cur_agg_vec = make_agg_vec(words=row, model=model, num_features=num_features,
                                                   model_word_set=model_word_set, filter_out=[])
                        writer.writerow([cur_id] + list(cur_agg_vec))

                        if prog_counter >= 0.05 * n_lines:
                            prog_counter = 0
                            update_progress(counter / (n_lines - 1))

                    except IndexError:

                        n_na += 1
                        pass
                print("\nFinished calculating aggregate document representations", "\nNumber of NA:", n_na)



