#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-19
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

learning_rate = 0.01
training_cnt = 10
display_step = 1

train_X1 = np.array([83., 63., 98., 77., 54.])
train_X2 = np.array([67., 88., 71., 99., 76.])
train_X3 = np.array([75., 96., 68., 67., 33.])
train_Y = np.array([144., 166., 172., 154., 112.])

X1 = tf.placeholder("float")
X2 = tf.placeholder("float")
X3 = tf.placeholder("float")
Y = tf.placeholder("float")

W1 = tf.Variable([.0], tf.float32, name = "weight1")
W2 = tf.Variable([.0], tf.float32, name = "weight2")
W3 = tf.Variable([.0], tf.float32, name = "weight2")
b = tf.Variable([.0], tf.float32, name = "bias")

pred = X1 * W1 + X2 * W2 + X3 * W3 + b

cost = tf.reduce_mean(tf.pow(pred-Y, 2))
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
op_train = optimizer.minimize(cost)

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)


for epoch in range(training_cnt):
    r_cost, r_W1, r_W2, r_W3, r_b,r_pred, _ = sess.run([cost, W1, W2, W3, b,pred, op_train], feed_dict = {X1: train_X1, X2: train_X2, X3: train_X3, Y: train_Y})
    if (epoch+1) % display_step == 0:

        print("Run_count : [%04d], Train_cost =[%.4f], W1 =[%.4f], W2 =[%.4f], W3 =[%.4f], b =[%.4f], pred =[%.4f %.4f %.4f %.4f %.4f]"
              % (epoch+1, r_cost, r_W1, r_W2, r_W3, r_b,r_pred[0],r_pred[1],r_pred[2],r_pred[3],r_pred[4] ))
        print("Optimization Finished!")
        print("Run_count : [%04d], Train_cost =[%.4f], W1 =[%.4f], W2 =[%.4f], W3 =[%.4f], b =[%.4f], pred =[%.4f %.4f %.4f %.4f %.4f]"
              % (epoch+1, r_cost, r_W1, r_W2, r_W3, r_b,r_pred[0],r_pred[1],r_pred[2],r_pred[3],r_pred[4] ))
