"""
NAME
    addr - This package contains interfaces and functionality to compute pair-wise document-dictionary
    similarities for a set of term-based dictionaries.
"""
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
from .simple_progress_bar import update_progress
from .file_length import file_len
from .get_vecs import get_files
from .get_vecs import make_agg_vec
from .get_vecs import doc_vecs_from_csv
from .get_vecs import doc_vecs_from_txt
from .get_vecs import terms_from_csv
from .get_vecs import terms_from_liwc
from .get_vecs import terms_from_txt
from .get_vecs import terms_to_csv
from .get_vecs import dic_vecs
from .get_vecs import write_dic_vecs
from .get_loadings import load_model
from .get_loadings import get_loadings





