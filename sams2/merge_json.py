#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-11

import json

f1 = open("/home/msl/ys/cute/data/sams2/save/entity_200_all_v2.json", "r")
f2 = open("/home/msl/ys/cute/data/sams2/save/random_questions_from_m4_5_to_6.json", "r")
d = dict()
d["version"] = "20190916"
d["data"] = list()

data = json.load(f1)
data2 = json.load(f2)
doc = data["data"]
doc2 = data2["data"]
d["data"].extend(doc)
d["data"].extend(doc2)
f3 = open("/home/msl/ys/cute/data/sams2/save/entity_and_random_question.json", "w")
json.dump(d, f3, ensure_ascii=False, indent = 2)
f1.close()
f2.close()
f3.close()