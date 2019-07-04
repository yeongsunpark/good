# -*- coding: utf-8 -*-


# Created by YeongsunPark at 2019-06-20

import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

import json

f = open("/home/minds/maum/resources/MRC/ys_result/sum2.json", "r")
json_data = json.load(f)
cate_dic = dict()
for j in json_data["data"]:
    cate = j["cate"]

    if cate in cate_dic:
        cate_dic[cate] +=1
    else:
        cate_dic[cate] =1

f.close()


import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
	def format(self, _object, context, maxlevels, level):
		if isinstance(_object, unicode):
			return "'%s'" % _object.encode('utf8'), True, False
		elif isinstance(_object, str):
			_object = unicode(_object,'utf8')
			return "'%s'" % _object.encode('utf8'), True, False
		return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)
MyPrettyPrinter().pprint(cate_dic)
print MyPrettyPrinter().pformat(cate_dic)