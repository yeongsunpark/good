#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-08

import pandas as pd
import os
import numpy as np
"""
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""
def get_df(sep='\t'):
    iter_tsv = pd.read_csv('aa.tsv', iterator=True, encoding='utf8', chunksize=1000, sep=sep)
    df = pd.concat([chunk for chunk in iter_tsv])
    return df
print (get_df(sep='\t'))



lst = [[1,2,3,4,5,6,7],
        [10,15,20,25,50,55,60],
        [0,0,0,0,0,0,0],
        [-1,-20,-30,-45,-50,-55,-70]]

df = pd.DataFrame(lst).T
print (df)
corr = df.corr(method = 'pearson')
print(corr)


df = pd.read_csv('aa.tsv', sep='\t')
df = df.loc[:,"a":]
corr = df.corr(method='pearson')
print (corr)
# print (df.ix[1])

# print (df.loc[:,"a":])
"""
"""
X = np.array([[0, -0.5], [-1.5, -1.5], [1, 0.5],  # 동그라미
              [-3.5, -2.5], [0, 1], [1, 1.5], [-2, -0.5]])  # 엑스
print ("X:", X)
y = np.array([1, 1, 1, 2, 2, 2, 2])
print ("y:", y)
x_new = [0, -1.5]  # 세모
print ("x_new:", x_new)
plt.scatter(X[y == 1, 0], X[y == 1, 1], s=100, marker='o', c='r', label="class 1")
print ("영선아!", X[y == 1, 0])
print ("안녕", y==1)
print ("영선아!", X[y == 1])
plt.scatter(X[y == 2, 0], X[y == 2, 1], s=100, marker='x', c='b', label="class 2")
plt.scatter(x_new[0], x_new[1], s=100, marker='^', c='g', label="test data") #
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("binary classify sample data")
plt.legend()
plt.show()
plt.savefig ("/home/msl/ys/cute/book/test_figure1.png",dpi=300)
"""
"""
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

x = range(0, 100)
y = [v*v for v in x]

ax1.plot(x, y)
ax2.bar(x, y)

try:
    plt.show()
    plt.savefig ("/home/msl/ys/cute/book/test_figure1.png",dpi=300)
except:
    print ("no")
"""
