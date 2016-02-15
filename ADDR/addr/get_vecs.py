from __future__ import division

__author__ = 'Joe Hoover'

import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import collections
import logging
from gensim.models import Word2Vec
import csv
import time as tm
from addr.file_length import file_len
import pandas as pd
from addr.simple_progress_bar import update_progress
#from addr.get_loadings import loadModel


def get_files(input_path):
    """Make dictionary of file paths from directory or list of directory. Keys are file names and are
    used to name dimensions represented in other functions. Can be used to build aggregate vectors for dictionaries
    or document corpora that are stored in individual files."""
    

    path_info = collections.OrderedDict()

    if os.path.isfile(input_path):
        f_name = input_path.split('/')[-1]
        path_info[f_name] = input_path

    else:
        for f in os.listdir(input_path):

            if os.path.isfile(os.path.join(input_path, f)) and not f.startswith('.'):
                path_info[f] = os.path.join(input_path, f)

            elif os.path.isdir(os.path.join(input_path, f)):
                sub_path = os.path.join(input_path, f)
                get_files(path=sub_path)

    return path_info


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



def doc_vecs_from_csv(input_path, output_path, model, num_features, model_word_set, text_col, filter_out = [], delimiter='\t',
                  id_col=False):
    """Make aggregate vectors from documents stored in CSV format. Write these to output file"""

    with open(input_path, 'rb') as docs_file, open(output_path, 'wb') as out_file:

        dialect = csv.Sniffer().sniff(docs_file.read(1024))
        docs_file.seek(0)

        check_header = csv.Sniffer().has_header(docs_file.read(1024))
        docs_file.seek(0)

        docs = csv.reader(docs_file, dialect)

        if check_header is True:
            print 'Header identified'

            header = docs.next()

            if id_col is not False:

                try:
                    id_col = header.index(id_col)

                except ValueError:

                    try:
                        id_col = int(id_col)

                    except ValueError:

                        print "ValueError: Column '{0}' not found, please make sure that the name or index was correctly listed".format(
                            id_col)
                try:

                    text_col = header.index(text_col)

                except ValueError:

                    try:
                        text_col = int(text_col)

                    except ValueError:

                        print "ValueError: Column '{0}' not found, please make sure that the name or index was correctly listed".format(
                            text_col)

            elif id_col is False:

                try:
                    text_col = header.index(text_col)

                except ValueError:

                    try:
                        text_col = int(text_col)

                    except ValueError:

                        print "ValueError: Column '{0}' not found, please make sure that the name or index was correctly listed".format(
                            text_col)
                        print header, head.index(text_col), text_col, int(text_col)

        if check_header is False:
            print 'No header identified'

            if id_col is not False:

                try:

                    id_col = int(id_col)

                except ValueError:

                    print "ValueError: Column '{0}' not found, please make sure that the index was correctly listed".format(
                        id_col)

                try:
                    text_col = int(text_col)

                except ValueError:

                    print "ValueError: Column '{0}' not found, please make sure that the index was correctly listed".format(
                        text_col)

            elif id_col is False:

                try:
                    text_col = int(text_col)

                except ValueError:

                    print "ValueError: Column '{0}' not found, please make sure that the index was correctly listed".format(
                        text_col)


        fieldnames = ['ID'] + [unicode(fnum) for fnum in range(1, num_features + 1)]
        writer = csv.writer(out_file, dialect, delimiter=delimiter)
        writer.writerow(fieldnames)


        n_lines = float(file_len(input_path))
        n_na = 0

        print 'Generating aggregate distributed representations of', n_lines, 'texts.'
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
                    cur_agg_vec = make_agg_vec(words=doc, model=model, num_features=num_features, model_word_set=model_word_set, filter_out = [])

                    writer.writerow([cur_id] + list(cur_agg_vec))

                    if prog_counter >= 0.05 * n_lines:
                        prog_counter = 0
                        update_progress(counter / (n_lines - 1))

                except IndexError:

                    n_na += 1
                    pass


        elif id_col is not False:

            for row in docs:

                try:

                    prog_counter += 1
                    counter += 1

                    doc = row[text_col].split()
                    cur_agg_vec = make_agg_vec(words=doc, model=model, num_features=num_features, model_word_set=model_word_set, filter_out = [])

                    writer.writerow([row[id_col]] + list(cur_agg_vec))

                    if prog_counter >= 0.05 * n_lines:
                        prog_counter = 0
                        update_progress(counter / (n_lines - 1))

                except IndexError:
                    n_na += 1
                    pass

            print "\nFinished calculating aggregate document representations", "\nNumber NA:", n_na





# getAggDocVecs(input_path='test_csv.csv', output_path='out_test.txt',
#               id_col='ID', text_col='text')

# Get aggregate vectors for documents stored in text format. Input can either be a single file, a directory,
# a directory of nested directories. If the input path is a directory/nested directory structure,
# all files contained in the directory/directories will be treated as single documents.


def doc_vecs_from_txt(input_path, output_path, num_features, model, model_word_set, delimiter='\t', filter_out = []):

    path_info = get_files(input_path=input_path)

    with open(output_path, 'wb') as out_file:

        fieldnames = ['ID'] + [unicode(fnum) for fnum in range(1, num_features + 1)]
        writer = csv.writer(out_file, delimiter=delimiter)
        writer.writerow(fieldnames)

        for input_path in path_info.itervalues():

            with open(input_path, 'rb') as docs:

                n_lines = float(file_len(input_path))

                print 'Generating aggregate distributed representations of', n_lines, 'texts.'
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
                print "\nFinished calculating aggregate document representations", "\nNumber of NA:", na_na



# Functions for getting aggregate dictionary vectors from various formats

# Read dictionary text files stored in nested directories into Python dictionary
# NOTE: Words in each file should be separated by only a space, no line breaks or commas.
def terms_from_txt(input_path):
    dic_terms_out = collections.OrderedDict()
    path_info = get_files(input_path=input_path)

    for k in path_info.iterkeys():
        current_file = path_info[k]

        with open(current_file, 'rb') as dict_file:
            dict_terms = list()
            dict_terms = dict_file.read()
            dict_terms = dict_terms.lower()
            dict_terms = dict_terms.split()
            dic_terms_out[k] = dict_terms

    return dic_terms_out



# Read LIWC-style term dictionary into Python dictionary

def terms_from_liwc(input_path):
    get_dims = 0
    with open(input_path, 'r') as document:

        out_dic = collections.defaultdict(list)
        codes = {}

        for line in document:
            line = line.split()
            if not line:  # empty line?
                continue

            if '%' in line:
                get_dims += 1

            if '%' not in line and get_dims == 1:
                codes[line[0]] = line[1]

            if get_dims == 2 and '%' not in line:
                words = []
                dims = []
                for el in line:
                    try:
                        int(el)
                    except ValueError:
                        words.append(el)

                    if el in codes.keys():

                        dims.append(el)

                for dim in dims:
                    out_dic[codes[dim]].extend(words)

    print "Number of dimensions registered: {0}".format(len(out_dic.keys()))
    print "Number of words registered: {0}".format(sum([len(i) for i in out_dic.values()]))
    return (out_dic)



# Read CSV file of dictionary terms into Python dictionary. Column names should represent the dimension associated
# with the words in the column

def terms_from_csv(input_path, delimiter):
    import pandas as pd
    dic_terms = pd.read_csv(input_path, delimiter)
    dic_terms.to_dict(orient='list')

    return dic_terms


#Write Python dictionary of terms to csv with column names as dimensions and cells as words
def terms_to_csv(terms_dic, output_path, delimiter='\t'):
    terms_dic = pd.DataFrame.from_dict(terms_dic, orient='columns')
    terms_dic.to_csv(output_path, sep=delimiter, index=False)



# Calculate aggregate dictionary vectors. Input must be a Python dictionary with key values pairings of dimension names (the keys)
# and the words representing the dimension (the values associated with each key).

def dic_vecs(dic_terms, model, num_features, model_word_set, filter_out=[]):
    agg_dic_vecs = collections.OrderedDict()
    for k in dic_terms.iterkeys():
        agg_dic_vecs[k] = make_agg_vec(dic_terms[k], model = model, num_features = num_features,
                                         model_word_set = model_word_set, filter_out = filter_out)

    return agg_dic_vecs

#dicVecs = dic_vecs(dic_terms=dic_terms_out)

# Write aggregate dictionary vectors to csv file. Input must be a dictionary of key values pairings where dimension names
# are keys and a vector of values is representing the dimension (as output by the dic_vecs() function.
# Column names are the key/dimension names and column contents are the vectors representing the dimension.

def write_dic_vecs(dic_vecs, output_path, delimiter='\t'):
    dic_vecs = pd.DataFrame.from_dict(dic_vecs, orient='columns')
    dic_vecs.to_csv(output_path, sep=delimiter, index=False)


# if __name__ == "__main__":
#
#     #if sys.argv[1] is
#
#
#     classify_text(dir=sys.argv[1], process_method = split_all, class_structure='independent')
#
#


