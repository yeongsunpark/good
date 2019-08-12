#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-16

from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Embedding, Dense, SimpleRNN
from keras.models import Sequential
from keras import optimizers
import numpy as np

model = Sequential()
model.add(Dense(3, input_dim = 4, activation = 'softmax'))
sgd = optimizers.SGD(lr=0.01)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X_train, y_train, batch_size=1, epoch=200, validation_data=(X_text, y_test))

epochs = range(1, len(history.history['acc']) + 1)
plt.plot(epochs, history.history['loss'])
plt.plot()