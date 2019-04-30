#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-03-19

import sys, logging
import ys.good.ys_logger as ys_logger
sys.path.append("/home/msl/ys/good/nia/")

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(ys_logger.MyHandler())
logger.info("Finish setting logger")


class Abc():
    def __init__(self):
        self.header = False
        self.result_list = []
        self.number = 0
        self.t = ""
        self.c = ""
        if len(sys.argv) ==1:
            self.f = open("/home/msl/ys/cute/nia/sw.txt", "r")
        else:
            self.f = open(sys.argv[1], "r")

    def main(self):
        for line in self.f:
            line = line.replace("\n", "")
            if self.header:
                self.header = False
                continue
            item = line.split("\t")
            if len(item) == 6:
                q_id = item[0]
                answer = item[3]
                c_id = item[4]
                context = item[5]

                answer_s = context.find(answer)
                logger.info("answer_s: %s" % answer_s)
                answer_e = answer_s + len(answer)
                extract_answer = context[answer_s:answer_e]
                self.number += 1
                if answer != extract_answer:
                    logger.info("answer_s: %s, answer_e: %s, answer: %s, extract_answer: %s" % answer_s, answer_e, answer, extract_answer)
                    break
                else:
                    self.result_list.append(
                        [str(q_id), str(answer_s), str(answer_e), str(answer), str(c_id), str(context)])
            else:
                logger.info("error%s" % item)
                break

        self.f.close()

        if len(sys.argv) == 1:
            f2 = open("/home/msl/ys/cute/nia/sw2.txt", "w")
        else:
            f2 = open(sys.argv[2], "w")
            logger.info("len: %s" % str(len(self.result_list)))
        for r in self.result_list:
            f2.write("\t".join(r))
            f2.write("\n")
        f2.close()
        logger.info("finish: %s" % str(self.number))

if __name__ == "__main__":
    j = Abc()
    j.main()
