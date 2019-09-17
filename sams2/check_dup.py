#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-16

import json

id_list = list()
print (id_list)
f = open("/home/msl/ys/cute/data/sams2/only_id.txt", "r")
f3 = open("/home/msl/ys/cute/data/sams2/only_id_dup.txt", "w")  # 중복된 데이터
for line in f:
    line = line.replace("\n","")
    flag = True
    if line in id_list:
        flag = False
        f3.write(line + "\n")
        f3.flush()
        # break
    if flag:
        id_list.append(line)
f.close()
f3.close()

# with open ("/home/msl/ys/cute/data/sams2/save/thank.json") as f1:
#     data = json.load(f1)
#     for d in data["data"]:
#         q_id = (d["paragraphs"][0]["qas"][0]["id"])
#         flag = True
#         if q_id in id_list:
#             flag = False
#             f3.write(q_id+"\n")
#         if flag:
#             id_list.append(q_id)
