#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-23

f = open("/home/msl/ys/cute/nia/common_tsv/크웍18전달건_편집_질문번호_ascending_num바꿈.txt", "r")
f2 = open("/home/msl/ys/cute/nia/common_tsv/크웍18전달건_편집_질문번호_ascending_num바꿈2.txt", "w")
a = 1
while True:
    line = f.readline()
    f2.write(line)
    if a == 3000:
        break
    a+=1
f.close()