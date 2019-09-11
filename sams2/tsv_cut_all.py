#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-05

def tsv_cut(j, start, end):
    f_in = open("/home/msl/ys/cute/data/sams2/entity_200_all_v2_ascend.txt", "r")
    i = 1
    f_out = open("/home/msl/ys/cute/data/sams2/" +"entity" + str(j) + ".txt", "w")
    lines = f_in.readlines()
    data = lines[start:end]
    for d in data:
        f_out.write(d)
    f_in.close()

if __name__ == '__main__':
    for i in range(0, 32060,10000):
        a = tsv_cut(i, i, i+10000)  # 단, 제일 끝은 하나 크게 하기.  # 2133 ~ 3145
    # a = tsv_cut(71261, 70000, 71261)