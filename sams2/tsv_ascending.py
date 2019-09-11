#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-29

# 오름차순으로 정렬
result_list = list()
with open("/home/msl/ys/cute/data/sams2/random_questions_from_m4_5_to_6.txt", "r") as f:
    for line in f:
        item = line.replace("\n","").split("\t")
        result_list.append(item)
    result_list.sort(key=lambda x : int(x[0].split("_")[-1]))
    result_list.sort(key=lambda x: x[0].split("_")[1])

f2 = open("/home/msl/ys/cute/data/sams2/random_questions_from_m4_5_to_6_ascend2.txt", "w")
for r in result_list:
    f2.write("\t".join(r))
    f2.write("\n")
f2.close()