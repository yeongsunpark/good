#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-03-12

import re
import sys

sys.path.insert(0, '')

# 사용방법: python3 trim_output.py /home/msl/ys/cute/nia/output.tsv /home/msl/ys/cute/nia/db_news/output2.tsv

result = []
with open (sys.argv[1]) as f:
    i = 0
    for line in f:
        item = line.split("\t")
        context = item[1]
        replace_list = ["&amp;", "&quot;", "&apos;", "&lt;", "&gt;"]
        for rl in replace_list:
            context = context.replace(rl,"")
        p = re.compile('[ ]{2,}')
        context = p.sub(' ',context)
        # length = len(context)

        if len(context) <= 301 or len(context) >= 2000:
            continue

        flag = True
        for i in range(len(result)):
            if context in result[i].split("\t")[1]:
                flag = False
                break
        if flag:
            result.append("\t".join([item[0], context]))

        # result.append("\t".join([item[0], context]))

f2 = open(sys.argv[2], "w")
for r in result:
    f2.write(r)
    # f2.write("\n")