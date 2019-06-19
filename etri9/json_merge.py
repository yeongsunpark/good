#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-17

import sys, os
import json

sys.path.insert(0,'..')

# 낱개 json 을 하나로
"""
# input_dir = "/home/msl/ys/cute/law/data4_out"
input_dir = "/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터"
output_file = "/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/sum.json"
# 하기 전에 txt 파일이 utf-8로 인코딩이 되어 있나 꼭 확인하기!
# utf-8 파일은 제일 윗 줄을 제대로 인식을 못하니 한 줄 띄기!


result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()

f2 = open(output_file, "w")
for f in os.listdir(input_dir):
    with open(os.path.join(input_dir, f), "r") as f:
        json_data1 = json.load(f)
        result['data'].append(json_data1)


with open ("sum.json","w") as f2:
    json.dump(result, f2, indent=2, ensure_ascii=False)
"""

# 법령 별 단락 수
"""
dic_title = dict()
with open("/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/pilot3.json", "r") as f1:
    d = f1.read()
    d = json.loads(d)
    for dd in (d["data"]):
        a = list(dd.keys())
        title = dd[a[0]]["법령명"]
        if title in dic_title:
            dic_title[title] += 1
        else:
            dic_title[title] = 1
print (dic_title)
"""

# 법령명이 기재된 문제수
"""
# with open("/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/pilot3.json", "r") as f1:
    z = 0
    d = f1.read()
    d = json.loads(d)
    for dd in (d["data"]):
        a = list(dd.keys())
        title = dd[a[0]]["법령명"]
        qas = dd[a[0]]["qas"]
        for qa in qas:
            q = qa["question"]
            title_nos = title.replace(" ","").replace("ㆍ","").replace("･","")
            q_nos = q.replace(" ", "").replace("ㆍ","").replace("･","")
            if title_nos not in q_nos:
                z +=1
    print (z)
            # else:
                # print("not in", qa["question"])
"""
# input_dir = "/home/msl/ys/cute/law/data4_out"
input_dir = "/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/json"
output_file = "/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/sum.json"
# 하기 전에 txt 파일이 utf-8로 인코딩이 되어 있나 꼭 확인하기!
# utf-8 파일은 제일 윗 줄을 제대로 인식을 못하니 한 줄 띄기!


result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()

f2 = open(output_file, "w")
for f in os.listdir(input_dir):
    with open(os.path.join(input_dir, f), "r") as f:
        json_data1 = json.load(f)
        json_data = json_data1['data']
        result['data'].extend(json_data)


with open ("/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/sum.json","w") as f2:
    json.dump(result, f2, indent=2, ensure_ascii=False)