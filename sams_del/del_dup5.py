#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-17

import sys, os
import re
import json
def del_dup(f2_name):
    result = {'version': 1, 'data': list()}
    input_dir = "/home/msl/ys/cute/data/sams2/dup/"
    f = open(input_dir + "use_id.txt", "r", encoding="utf-8")
    lines = f.readlines()
    lst = list()
    with open(input_dir + f2_name, "r", encoding="utf-8") as f2:
        json_data = json.load(f2)
        for data in json_data["data"]:
            flag = False
            for p in data["paragraphs"]:
                for q in p["qas"]:
                    q_id = q["id"]
                    for line in lines:
                        """
                        if q_id == line.replace("\n", ""):
                            # print (q_id)
                            result['data'].append(data)
                            # print (len(data))
                            break
                        """
                        if q_id == line.replace("\n",""):
                            flag = True
                            break
                    if not flag:
                        # print (q_id)
                        result['data'].append(data)
                        lst.append(q_id)
                        break
    f.close()
    with open(input_dir + "only_" + f2_name, "w", encoding="utf-8") as f3:
        json.dump(result, f3, ensure_ascii=False, indent=2)
    f5 = open(input_dir + "use_id.txt", "a", encoding="utf-8")
    for l in lst:
        f5.write(l)
        f5.write("\n")
    f5.close()
if __name__ == '__main__':
    del_dup("dup_number15.json")
