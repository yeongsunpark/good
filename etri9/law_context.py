#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-29

import os, sys, logging
sys.path.append(os.path.abspath('..'))
import ys.good.ys_logger as ys_logger

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(ys_logger.MyHandler())
logger.info("Finish setting logger")

input_dir = "/home/msl/ys/cute/data/law"
logging.basicConfig(filename='%s/example.log'%input_dir,level=logging.INFO,
                    format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >>> %(message)s')
for f in os.listdir(input_dir):
    if "txt" not in f:
        continue
    else:
        with open(os.path.join(input_dir, f), "r") as f1:
            logger.info("open file: %s" % f)
            d = f1.readlines()
            data = '{"1":['
            for i in range(len(d)):
                data += d[i]
            data = data.replace("}", "},")
            data += "]}"
            data = data.replace("\n", "")
            data = data.replace("  ", "")
            data = data.replace("]},]}", "]}]}")

        with open((os.path.join(input_dir, "output/{}_result.json").format(f.split(".")[0])), "w") as f2:
            f2.write(data)
            logger.info("save file: %s" % f)
        os.system("mv {input_dir}/{file} {input_dir}/used/".format(input_dir=input_dir, file=f))