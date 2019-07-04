#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-20
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random

import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
	def format(self, _object, context, maxlevels, level):
		if isinstance(_object, unicode):
			return "'%s'" % _object.encode('utf8'), True, False
		elif isinstance(_object, str):
			_object = unicode(_object,'utf8')
			return "'%s'" % _object.encode('utf8'), True, False
		return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)


result = dict()
result['version'] = "1"
result['creator'] = "MINDs Lab."
# result['data'] = list()

f = open("/home/minds/maum/resources/MRC/ys_result/sum2.json", "r")
json_data = json.load(f)
cate_dic = dict()

cnt = 1
for i in ["IT/과학", "노컷경제", "사회", "세계", "스포츠", "연예", "정치", "지역"]:
# for i in ["경제", "국제", "문화", "미래&과학", "사회", "스포츠", "정치"]:
# for i in ["경제/산업"]:
    result['data'] = list()
    pre_result = dict()
    pre_result['data'] = list()
    for j in json_data["data"]:
        if j["cate"] == i:
            pre_result['data'].append(j)
    if i == "IT/과학":
        a = pre_result["data"]
    else:
        a = random.sample(list(pre_result["data"]), 1000)
    result['data'].extend(a)
    f2 = open("/home/minds/maum/resources/MRC/ys_result/sum2_{}.json".format(cnt), "w")
    json.dump(result, f2, indent=2, ensure_ascii=False)
    f.close()
    f2.close()
    cnt +=1
# print MyPrettyPrinter().pformat(result)

"""
f2 = open("/home/minds/maum/resources/MRC/ys_result/sum2_7276.json", "w")
json.dump(result, f2, indent=2, ensure_ascii=False)
f.close()
f2.close()
"""