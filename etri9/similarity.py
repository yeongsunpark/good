#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-03

from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from numpy.linalg import norm
import numpy as np
import re

def cos_sim(A, B):
       return dot(A, B)/(norm(A)*norm(B))

corpus = [
    '''만들 목적''',
    '''만들''',
    '''만들 목적''',
    '''목적 만들''',
]

tfidfv = TfidfVectorizer().fit(corpus)
print(tfidfv.transform(corpus).toarray())
print(tfidfv.vocabulary_)


print (type(corpus[0]))
context = np.array(tfidfv.transform(corpus).toarray()[0])
q1 = np.array(tfidfv.transform(corpus).toarray()[1])  # 상
q2 = np.array(tfidfv.transform(corpus).toarray()[2])
q3 = np.array(tfidfv.transform(corpus).toarray()[3])

print (cos_sim(context, q1))
print (cos_sim(context, q2))
print (cos_sim(context, q3))
