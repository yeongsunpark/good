#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-29

import os, sys
import json

input_dir = "/home/msl/ys/cute/data/law"
for f in os.listdir(input_dir):
    if "result" in f:
        continue
    else:
        with open(os.path.join(input_dir, f), "r") as f1:
            d = f1.readlines()
            data = '{"1":['
            for i in range(len(d)):
                data += d[i]
            data = data.replace("}", "},")
            data += "]}"
            data = data.replace("\n", "")
            data = data.replace("  ", "")
            data = data.replace("]},]}", "]}]}")

    with open((os.path.join(input_dir, "/output/{}_result.json").format(f.split(".")[0])), "w") as f2:
        # json.dumps(data, f2, indent = 2, ensure_ascii=False)
        f2.write(data)