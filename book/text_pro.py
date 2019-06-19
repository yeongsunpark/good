#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-11

import nltk
from nltk.tokenize import word_tokenize  # 단어 토큰화
from nltk.tokenize import WordPunctTokenizer # 단어 토큰화2
from nltk.tokenize import TreebankWordTokenizer  # 단어 토큰화2
from nltk.tokenize import sent_tokenize  # 문장 토큰화
from nltk.tag import pos_tag  # 품사 부착
from konlpy.tag import Okt # 한국어 형태소 토큰화
from nltk.stem import WordNetLemmatizer # 표제어 추출

import pandas as pd
from collections import Counter

from keras_preprocessing.text import Tokenizer # keras를 이용한 단어 토큰화
from keras.utils import to_categorical # keras 를 이용한 원-핫 인코딩

import re
"""
# bag of word
okt = Okt()

token = re.sub("(\.)", "", "정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다.")
token = okt.morphs(token)

word2index = {}
bow = []
for voca in token:
    if voca not in word2index.keys():
        word2index[voca] = len(word2index)
        print ("word2index:", word2index)
        bow.insert(len(word2index)-1, 1)
        print("bow:", bow)
    else:
        index = word2index.get(voca)
        print ("index:", index)
        bow[index]=bow[index]+1
        print ("bow:", bow)
print (word2index)
"""

from sklearn.feature_extraction.text import CountVectorizer # tdm
from sklearn.feature_extraction.text import TfidfVectorizer  # tf-idf

from numpy import dot
from numpy.linalg import norm
import numpy as np
def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
data = pd.read_csv('현재 metadata.csv의 파일 경로', low_memory=False)
data.head(2)
data = data.head(1000)
tfidf = TfidfVectorizer(stor_words="english")
data['overview'] = data['overvies'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['overview'])
print(tfidf_matrix.shape)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(data.index, indx=data['title']).drop_duplicates()
idx = indices['Father of the Bride Part']