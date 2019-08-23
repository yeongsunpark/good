#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-19
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

### 모델 구축
# 파라메터
learning_rate = 0.01
training_cnt = 10
# 트레이닝 변수 선언
train_X = np.array([1, 2, 3])
train_Y = np.array([1, 2, 3])
# tf graph input
X = tf.placeholder("float")  # placeholder: 학습용 데이터 담는 그릇
Y = tf.placeholder("float")
# set model weight
W = tf.Variable([.0], tf.float32, name = "weight") # 초기값, data type, 이름
b = tf.Variable([.0], tf.float32, name = "bias")
# construct a linear model (Wx+b)
pred = tf.add(tf.multiply(X, W), b)  # pred = X * W + b
# cost loss function
# reduce mean 은 들어오는 입력의 평균 값을 구함.
cost = tf.reduce_mean(tf.pow(pred-Y, 2))  # cost = tf.reduce_mean(tf.square(pred - Y)
optimizer = tf.train.GradientDescentOptimizer(learning_rate)  # cost 최소화 하는 학습 방법 사용. 경사하강법
op_train = optimizer.minimize(cost)

### 모델 실행
# tf 세션 생성
sess = tf.Session()
# 변수들에 초기값 할당
init = tf.global_variables_initializer()
sess.run(init)
for epoch in range(training_cnt):
    # sess.run 을 통해 학습한 cost, W, b 값을 r_cost, r_W, r_b 에 업데이트.
    r_cost, r_W, r_b, _ = sess.run([cost, W, b, op_train], feed_dict = {X: train_X, Y: train_Y})
    print("Running count : " '%04d' % (epoch+1), "Training cost =", r_cost, "W =", r_W, "b =", r_b)
    print("Optimization Finished!")
    print("Running count : " '%04d' % (epoch+1), "Training cost =", r_cost, "W =", r_W, "b =", r_b)