#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-15

import os, sys
import json

input_dir = "/home/msl/ys/cute/data/re_law/답과3가지질문만들기-1차(1474건)"
output_file = "/home/msl/ys/cute/data/re_law/답과3가지질문만들기-1차(1474건)2"

add_file = "/home/msl/ys/cute/data/re_law/김혜성_임시법률 - 시트1 (1).tsv"
with open (add_file) as af:
    for aff in af:
        item = aff.split("\t")
        if len(item) == 3:
            law_name = item[0]
            title = item[1]
            memo = item[2]

            for fl in os.listdir(input_dir):
                with open(os.path.join(input_dir, fl), "r") as f:
                    if "swp" in fl:
                        continue
                    name = fl.split("_")[0]
                    json_data1 = json.load(f)
                    json_data = json_data1[name]
                    f_law_name = json_data["법령명"]
                    f_title = json_data["조제목"]
                    if law_name == f_law_name and title == f_title:
                        json_data["메모"] = memo
                        with open(os.path.join(output_file, fl), "w") as f2:
                            json_data1[name] = json_data
                            json.dump(json_data1, f2, indent=2, ensure_ascii=False)
                        os.system("rm /home/msl/ys/cute/data/re_law/답과3가지질문만들기-1차\(1474건\)/{}".format(fl))
