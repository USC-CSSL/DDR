__author__ = 'joe'

import os
import collections
import pandas as pd

def get_files(input_path):
    """

    :param input_path: Directory containing term file(s)
    :return: A dictionary of file paths. Keys are file names and are used to
    name dimensions represented in other functions
    """


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
                get_files(input_path=sub_path)

    return path_info


def terms_from_txt(input_path):
    '''

    :param input_path: Path to directory containing term file(s)
    :return: A dictionary with dimension names as keys and words as values.
    '''
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


def terms_from_liwc(input_path):
    '''
    Read LIWC format dictionary into Python dictionary format

    :param input_path: Path to LIWC dictionary
    :return: A dictionary with dimension names as keys and words as values.
    '''

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

    print("Number of dimensions registered: {0}".format(len(out_dic.keys())))
    print("Number of words registered: {0}".format(sum([len(i) for i in out_dic.values()])))
    return (out_dic)



# Read CSV file of dictionary terms into Python dictionary. Column names should represent the dimension associated
# with the words in the column

def terms_from_csv(input_path, delimiter):
    '''
    Read CSV file of dictionary terms into Python dictionary. Column names should represent the dimension associated
    with the words in the column.
    :param input_path: Path to csv
    :param delimiter: delimiter used in csv file
    :return: A dictionary with csv column names as keys and words as values.
    '''
    import pandas as pd
    dic_terms = pd.read_csv(input_path, delimiter)
    dic_terms.to_dict(orient='list')

    return dic_terms

def terms_to_csv(terms_dic, output_path, delimiter='\t'):
    '''
    Write Python dictionary of terms to csv with column names as dimensions and cells as words

    :param terms_dic: Dictionary of terms where keys are dimension names and values are terms
    :param output_path: Path to output file
    :param delimiter: Delimiter to use for output
    :return: None.
    '''

    terms_dic = pd.DataFrame.from_dict(terms_dic, orient='columns')
    terms_dic.to_csv(output_path, sep=delimiter, index=False)
