#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-22

import os, sys
import json
import re


input_dir = "/home/msl/ys/cute/data/re_law/답과3가지질문만들기-1차(1474건)"
output_dir = "/home/msl/ys/cute/data/re_law/dupli"
dup_list = ["167", "170", "181", "193", "200", "205", "206", "208", "209", "212", "214", "216", "218", "219", "221", "225", "243", "244"]

for fl in os.listdir(input_dir):
    with open(os.path.join(input_dir, fl), "r") as f:
        for dl in dup_list:
            my_regex = r"^" + re.escape(dl) + r"[_]"
            if re.search(my_regex,fl):
                ind = input_dir.replace("(", "\(").replace(")", "\)")
                os.system ("cp %s/%s %s" % (str(ind), str(fl), str(output_dir)))
                os.system("mv %s/%s %s/1_%s" % (str(output_dir), str(fl), str(output_dir), str(fl)))