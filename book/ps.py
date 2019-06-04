#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-16

from keras.preprocessing.text import Tokenizer
t = Tokenizer()
fit_text = "The earth is an awesome place live"
t.fit_on_texts([fit_text])

test_text = "The earth is an great place live"
sequences = t.texts_to_sequences([test_text])[0]

print ("sequences:", sequences, '\n')
print("word_index:", t.word_index)


sentences = []
sentence = []
ner_set = set()
for line in f:
    if len(line) ==0 or line.startswith('-DOCSTART') or line[0] == "\n":
        if len(sentence) > 0:
            sentence.append(sentence)
        continue
    splits = line.split(" ")
    splits[-1] = re.sub(r'\n', "", splits[-1])
    word = splits[0].lower()
    vocab[word] = vocab[word]+1
    sentence.append([word, splits[-1]])
