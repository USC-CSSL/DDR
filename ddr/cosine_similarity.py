__author__ = 'joe'

import operator
import math

import numpy as np


def cos_similarity(v1, v2):
    prod = np.dot(v1, v2)
    len1 = math.sqrt(np.dot(v1, v1))
    len2 = math.sqrt(np.dot(v2, v2))
    return prod / (len1 * len2)
