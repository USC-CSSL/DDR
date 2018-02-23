__author__ = 'joe'

import collections
import sys


def ddr_neighbors(dictionary_terms, model, n=2):

    fields = dictionary_terms.keys()
    ddr_neighbors_dic = collections.OrderedDict((el, []) for el in fields)

    for k in dictionary_terms.keys():
        print("Querying nearest neighbors for {0}".format(k))
        sim = model.most_similar(dictionary_terms[k], topn=n)

        for word in sim:
            ddr_neighbors_dic[k].append(word[0])

    print('finished')
    return ddr_neighbors_dic



