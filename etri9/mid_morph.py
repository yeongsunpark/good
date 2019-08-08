#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-07
# tsv 파일을 하나로 취합 + 작업 하기

import sys, os
import re

input_dir = "/home/msl/ys/cute/data/mid_morph"
open_dir = os.listdir("/home/msl/ys/cute/data/mid_morph")
no_nlp_result = list()
no_dup_result = list()

for file in open_dir:
    header = True
    with open("/home/msl/ys/cute/data/mid_morph/{}".format(file), "r") as f:
        if "형태소분석_mid_20190807" not in file or "re" in file:
            continue
        # result = list()  # 낱개로 저장할 때
        data = f.readlines()
        for d in data:
            if header:
                header = False
                continue
            d = d.replace("\n", "")
            item = d.split("\t")
            for i in range(len(item)):
                if item[i].startswith('"') and item[i].endswith('"'):
                    item[i] = item[i].strip('"')
                item[i] = item[i].strip()

            if len(item) >=5:
                # print (item)
                id = item[0]
                use_text = item[1]
                nlp3 = item[2]
                correction_text = item[3]
                if correction_text != "":
                    use_text = correction_text
                    nlp3 = ""
                    no_nlp_result.append([id, use_text])
                nlp_work = item[4]
                # result.append([id, use_text, nlp3, nlp_work])  # 낱개로 저장할 때

                # 중복제거
                flag = True
                for i in range(len(no_dup_result)):
                    if use_text in no_dup_result[i][1]:
                        flag = False
                        break
                if flag:
                    no_dup_result.append([id, use_text, nlp3, nlp_work])

            # 낱개로 저장할 때
            # with open("/home/msl/ys/cute/data/mid_morph/re_{}".format(file), "w") as f2:
                # for r in result:
                    # f2.write("\t".join(r))
                    # f2.write("\n")
# 띄어쓰기 등의 이유로 형태소 분석기 다시 돌려야 하는 것.
with open("/home/msl/ys/cute/data/mid_morph/no_nlp.tsv", "w") as f3:
    for r in no_nlp_result:
        f3.write("\t".join(r))
        f3.write("\n")

# 중복제거한 파일
with open("/home/msl/ys/cute/data/mid_morph/only_nlp.tsv", "w") as f4:
    for r in no_dup_result:
        f4.write("\t".join(r))
        f4.write("\n")