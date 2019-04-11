#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by YeongsunPark at 2019-02-27
import sys, os
import json
import time
import check_wh

lst = []
with open("wh-no_wh.txt", "r") as f1:
    for ff in f1:
        ff = ff.replace("\n","")
        i = ff.split("\t")
        l = i[0], i[1]
        lst.append(l)

result = []
with open("new_normal_finish-sum.txt", "r") as f:
    # TITLE context 질문번호    질문    답변    카테고리    육하원칙    원본    답 시작위치 답 끝위치
    for line in f:
        line = line.replace("\n","")
        item = line.strip().split("\t")
        q = item[3]
        w = item[6]
        flag = True
        if w == "":
            for l in lst:
                if q == l[0]:
                    flag = False
                    result.append([item[0], item[1], item[2], item[3], item[4], item[5], l[1], item[7], item[8], item[9]])
                    break
            if flag:
                result.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]])
        else:
            result.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]])

f2 = open("new_normal_finish-sum2.txt", "w")
for r in result:
    f2.write("\t".join(r))
    f2.write("\n")

f2.close()

