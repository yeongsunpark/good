#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-08

import sys, os
import re

open_dir = "/home/msl/ys/cute/data/mid_morph"
# left_f = os.path.join(open_dir, "no_nlp_result.tsv", "r")
# join_f = os.path.join(open_dir, "result.tsv", "w")

result = list()
with open (os.path.join(open_dir, "only_nlp.tsv"), "r") as right_f:
    right_data = right_f.readlines()
    for r_d in right_data:
        item = r_d.replace("\n","").split("\t")
        id = item[0]
        use_text = item[1]
        nlp3 = item[2]
        correction_text = item[3]
        if nlp3 == "":
            with open(os.path.join(open_dir, "no_nlp_result.tsv"), "r") as left_f:
                left_data = left_f.readlines()
                for l_d in left_data:
                    item = l_d.replace("\n", "").split("\t")
                    l_use_text = item[0]
                    l_nlp3 = item[1]
                    if use_text == l_use_text:
                        nlp3 = l_nlp3
                        break
        result.append([id, use_text, nlp3, correction_text])

with open(os.path.join(open_dir, "final.tsv"), "w") as final:
    for r in result:
        final.write("\t".join(r))
        final.write("\n")



