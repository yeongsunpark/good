#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-28
import sys, os
import json

result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()

fff = "nine"


open_dir = os.listdir("/home/msl/ys/cute/data/wiki/mindslab_distribution_190617/zero/{}".format(fff))
for files in open_dir:
    # with open ("/home/msl/ys/cute/data/wiki/mindslab_distribution_190617/251019600000000.txt", "r") as f:
    with open ("/home/msl/ys/cute/data/wiki/mindslab_distribution_190617/zero/{}/{}".format(fff, files), "r") as f:
        data = f.readlines()
        title = data[0]
        content = ""
        pre_result = dict()
        pre_result['contents'] = list()
        pre_result['title'] = list()

        for d in data[1:]:
            if "paragraphID" in d:
                paragraphID = d.strip("\n").split(": ")[1]
            else:
                content = d.strip("\n")
                if len(content) < 50:
                    content = ""
            if content != "":
                # print (paragraphID, content)
                contents = dict()
                contents['paragraphID'] = paragraphID
                contents['content'] = content
                # result['data'].append([paragraphID, content])
                pre_result['contents'].append(contents)
        pre_result['title'] = title.strip()
        result['data'].append(pre_result)
    # f2 = open("/home/msl/ys/cute/data/wiki/json/{}.json".format(str(files.split(".")[0])), 'w', encoding='utf-8')
f2 = open("/home/msl/ys/cute/data/wiki/json/zero_{}.json".format(fff), 'w', encoding='utf-8')
json.dump(result, f2, ensure_ascii=False, indent=2)
f2.close()