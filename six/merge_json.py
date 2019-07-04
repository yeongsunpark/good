#-*- coding: utf-8 -*-
# !/usr/bin/env python

# Created by YeongsunPark at 2019-06-20

import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

import json

input_dir = "/home/minds/maum/resources/MRC/ys_output"
# output_file = "/home/minds/maum/resources/MRC/ys_result/sum.json"

result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()
# f2 = open(output_file, "w")
for f in os.listdir(input_dir):
    with open(os.path.join(input_dir, f), "r") as f:
        json_data1 = json.load(f)
        json_data = json_data1["data"]
        # print (json_data)
        #print (json_data1.decode('utf-8').encode('utf-8'))
        result['data'].extend(json_data)
with open("/home/minds/maum/resources/MRC/ys_result/sum2.json", "w") as f2:
    json.dump(result, f2, indent=2, ensure_ascii=False)