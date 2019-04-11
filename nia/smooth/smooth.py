#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-03-26


f1 = open("sum_no_checker.tsv", "r")
# 박영선  a
# 이원문  b
# 카카오  c
# 박영선  d
# 이원문  e
lst = list()
l1 = list
for ff in f1:
    ff = ff.replace("\n", "")
    i = ff.split("\t")
    wh = i[2]
    question = i[3]
    answer = i[4]
    l1 = wh, question, answer
    lst.append(l1)
f1.close()
print ("Finish load f1")


f2 = open("new_normal_finish-sum.txt", "w")
result = []
with open("normal_finish-sum.tsv", "r") as f:
    # 박영선  parkys  a
    # 이원문  moon    b
    # 카카오  kakao   c
    # 박영선  ylunar  x
    # 이원문  moon    y

    for line in f:
        line = line.replace("\n","")
        item = line.split("\t")
        q = item[3]
        a = item[4]
        flag = True

        for l in lst:
            # for s1, i in zip(select_data1, range(len(select_data1))):
            if q == l[1]:
                flag = False
                result.append([item[0], item[1], item[2], item[3], item[4], item[5], l[0], item[7], item[8], item[9]])
                break
        if flag:
            result.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]])

for r in result:
    f2.write("\t".join(r))
    f2.write("\n")

f2.close()
print ("Finish All")