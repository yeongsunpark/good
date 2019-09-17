#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-17

import sys, os
import re
import json
def del_dup(f2_name):
    input_dir = "/home/msl/ys/cute/data/sams2/"
    f = open(input_dir + "only_id_dup.txt", "r", encoding="utf-8")
    lines = f.readlines()
    is_find = False
    with open(input_dir + f2_name, "r", encoding="utf-8") as f2:
        json_data = json.load(f2)
        for data in json_data["data"]:
            for p in data["paragraphs"]:
                for q in p["qas"]:
                    q_id = q["id"]
                    for line in lines:
                        if q_id == line.replace("\n", ""):
                            print (q_id)
                            # print (json_data["data"][0]["paragraphs"][0]["qas"][0])
                            is_find = True
                            break
                    if is_find is True:
                        break

                if is_find is True:
                    break
            if is_find is True:
                del data['paragraphs']
                is_find = False

                """
                    for line in lines:
                        if q_id == line.replace("\n",""):
                            print (q_id)
                            print (line.replace("\n",""))
                            print(json_data["data"][0])
                            del json_data["data"][0]
                            # break
                """

    f.close()
    # with open(input_dir + "clean/clean_" + f2_name, "w", encoding="utf-8") as f3:
        # json.dump(json_data, f3, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    del_dup("number12.json")
