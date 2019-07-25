#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-28
# 전처리
import sys, os
import json
import re

result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()

#
re1 = re.compile(r".*다[.][ ]*$")
re2 = re.compile(r".*다\(.*\)[.]")

# delete list
re3 = re.compile(r"- ↑.*")
re4 = re.compile(r".* 목록이다[.]")
re5 = re.compile(r".*\{.*\}.*")
re6 = re.compile(r".*¶.*")

fff = "six"
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
                if re1.match(content):
                    content = content
                elif re2.match(content):
                    content = content
                else:
                    content = ""
                content = re3.sub("", content)
                content = re4.sub("", content)
                content = re5.sub("", content)
                content = re6.sub("", content)
                if len(content) < 50:
                    content = ""
                if content.startswith("*") or content.startswith(";") or \
                    content.startswith(":") or content.startswith("#") or \
                    content.startswith("|") or content.startswith("{") or \
                    content.startswith("-"):
                    content = ""
            if content != "":
                contents = dict()
                contents['paragraphID'] = paragraphID
                contents['content'] = content
                pre_result['contents'].append(contents)
            if content != "" and "목록" not in title:
                pre_result['title'] = title.strip()
        if pre_result['title']:
            result['data'].append(pre_result)

    # f2 = open("/home/msl/ys/cute/data/wiki/json/{}.json".format(str(files.split(".")[0])), 'w', encoding='utf-8')
f2 = open("/home/msl/ys/cute/data/wiki/refined_json/zero_{}.json".format(fff), 'w', encoding='utf-8')
json.dump(result, f2, ensure_ascii=False, indent=2)
f2.close()