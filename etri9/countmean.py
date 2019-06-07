#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-03

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

df = pd.read_csv("/home/msl/ys/cute/data/cw0530/result_morp/recall.txt", error_bad_lines=False, sep='\t', header = None)

def make(number):
    new_df = [[] for _ in range(len(df))]  # 큰 리스트 안에 603개의 작은 리스트를 만듦.
    a = 0
    for i in range(len(df)):  # 603번을 반복하는데,
        if i % 3 == number:  # 상번째일 때, 중번째일 때, 하번째일 때
            new_df[a].append(df.loc[i][0])  # 상번째일 때만 a번째 리스트에다가 값을 넣고,
            new_df[a].append(df.loc[i][1])
        a += 1  # 다음 리스트로 가기 위한.

    double_list = []
    for i in range(len(new_df)):
        if new_df[i]:  # new_df 에 값이 있으면, 즉 상번째였으면.
            double_list.append(new_df[i])  # 더블리스트에 넣고.
    return double_list

sang_list = make(0)  # 0.655
joong_list = make(1)  # 0.603
ha_list = make(2)  # 0.713



for i, lst in enumerate ([sang_list, joong_list, ha_list]):
    df = pd.DataFrame(lst)
    print (np.mean(df[1]))
    x = np.array(df[1])
    plt.title("hist_%s" % str(i))
    arrays, bins, patches = plt.hist(x, bins=20)
    plt.show()
    plt.savefig("/home/msl/ys/cute/data/cw0530/result_morp/hist_%s.png" % str(i))