#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-18

import json
import os
write_json = "clean_number22.json"

file_names = os.listdir("/home/msl/ys/cute/data/sams2/dup")
result = {'version': 1, 'data': list()}
for file_name in file_names:
    if not "only_dup" in file_name:
        continue
    else:
        full_name = os.path.join("/home/msl/ys/cute/data/sams2/dup", file_name)
        print (full_name)
        with open(full_name, 'r', encoding='utf-8') as f1:
            json_data1 = json.load(f1)
            result['data'].extend(json_data1['data'])

with open(os.path.join("/home/msl/ys/cute/data/sams2/dup", write_json), "w", encoding='utf-8') as wf:
    json.dump(result, wf, ensure_ascii=False, indent=2)