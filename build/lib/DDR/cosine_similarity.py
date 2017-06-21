__author__ = 'joe'

import operator
import math

def dot_product2(v1, v2):
    return sum(map(operator.mul, v1, v2))


def cos_similarity(v1, v2):
    prod = dot_product2(v1, v2)
    len1 = math.sqrt(dot_product2(v1, v1))
    len2 = math.sqrt(dot_product2(v2, v2))
    return prod / (len1 * len2)