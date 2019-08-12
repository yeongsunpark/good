#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-08

import os, sys
import logging
sys.path.insert(0,'..')
import ys_logger
from marker_checker import marker_checker
from three_checker import three_checker
from comp_with_ori import comp_with_ori

# log
logger = logging.getLogger('root')
logger.setLevel("DEBUG") # INFO
logger.addHandler(ys_logger.MyHandler())
logger.info("All finished")


class check():
    def __init__(self):
        self.input_dir = "/home/msl/ys/cute/data/sams"

    def main(self):
        for f in os.listdir(self.input_dir):
            if "2" in f:
                continue
            header = True
            logger.info("File {} start..".format(f))

            with open(os.path.join(self.input_dir, f), "r") as f:
                for ind, line in enumerate(f):
                    if header:
                        header = False
                        continue

                    item = line.strip().split("\t")
                    if len(item) == 11:
                        q_id = item[0]
                        context = item[1]
                        question = item[2]
                        answer = item[3]
                        classify = item[4]
                        mod_question = item[5]
                        mod_answer = item[6]
                        mod_context = item[7]
                        remarks = item[8]
                    else:
                        logger.error("Check len item")
                        break
                    # marker_checker(ind, context)  # 마커 개수 확인
                    # three_checker(ind, classify, mod_question, mod_answer, mod_context)  # 분류와 체커 확인
                    comp_with_ori(ind, q_id, context, question, answer, mod_question, mod_answer, mod_context, remarks)  # 원본과 비교


if __name__ == '__main__':
    c = check()
    c.main()
