#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-02
import sys, os
import json

open_dir = os.listdir("/home/msl/ys/cute/data/news")
for files in open_dir:
    if "sum2_7276.json" in files:
        with open ("/home/msl/ys/cute/data/news/{}".format(files)) as f:
            d = f.read()
            data = json.loads(d)
            for a in data["data"]:
                print (len(a["content"]))
                # break
