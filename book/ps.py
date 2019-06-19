#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-16

from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Embedding, Dense, SimpleRNN
from keras.models import Sequential
import numpy as np

t = Tokenizer()
text="""경마장에 있는 말이 뛰고 있다\n
그의 말이 법이다\n
가는 말이 고와야 오는 말이 곱다\n"""
t.fit_on_texts([text])
encoded = t.texts_to_sequences([text])[0]  # [2, 1, 3, 4, 5, 6, 1, 7, 8]
# print (encoded)

vocab_size = len(t.word_index) +1  # 단어 집합의 크기 (9)
sorted(t.word_index.items(), key=lambda item: item[1])  # [('점심', 1), ('나랑', 2), ('먹으러', 3), ('갈래', 4), ('메뉴는', 5), ('마라탕', 6), ('메뉴', 7), ('좋지', 8)]

sequences = list()
for line in text.split("\n"):
    encoded = t.texts_to_sequences([line])[0]
    for i in range(1, len(encoded)):
        sequence = encoded[:i+1]
        sequences.append(sequence)
print (sequences)

maxlen = max(len(l) for l in sequences)

sequences = pad_sequences(sequences, maxlen=maxlen, padding='pre')
print (sequences)
sequences = np.array(sequences)
X = sequences[:, :-1]
y = sequences[:, -1]

# y에 대한 원-핫 인코딩
y = to_categorical(y, num_classes=vocab_size)

model = Sequential()
model.add(Embedding(vocab_size, 10, input_length=5))
model.add(SimpleRNN(32))
model.add(Dense(vocab_size, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=20, verbose=2)