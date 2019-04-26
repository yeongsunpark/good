#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-25

import json

f = open("/home/msl/ys/cute/nia/check/ko_nia_v0425_squad_pretty_train.json", "r")
j = f.read()
j = json.loads(j)
data = j['data']
c = dict()
for d in data:
    for qa, i in zip(d['paragraphs'][0]['qas'], range(len(d['paragraphs'][0]['qas']))):
        classType = qa['classtype']

        if classType in c:
            c[classType] +=1
        else:
            c[classType] = 1
print (c)
f.close()