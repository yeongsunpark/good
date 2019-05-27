#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-23

import logging
import os, sys
import pymysql
sys.path.append(os.path.abspath('..'))
from pull_module import SquadDbSuper
import csv

class SquadDb(SquadDbSuper):
    def __init__(self):
        super(SquadDb, self).__init__()

    def connect_db2(self):
        cfg_dict = self.connect_db()
        self.cur = self.easy_mysql(cfg_dict)

    def line2item(self, line):
        line = line.replace("\n","")
        item = line.split("\t")
        return item

    def update_wh(self):
        wh_dict = {"work_who":0, "work_when":1, "work_where":2, "work_what":3, "work_how":4, "work_why":5}
        f = open("/home/msl/ys/cute/nia/text/no_wh27_result.txt" ,"r")
        for line in f:
            item = self.line2item(line)

            c_id = item[0]
            q_id = item[1]
            q_id2 = q_id.split("-")[0]+"-2"
            question = item[2]
            classType = "work_"+(item[3])
            numType = wh_dict[classType]

            try:
                update_memo_sql = "update all_qna_error set classType = %s, numType = %s where q_id = %s"
                self.cur.execute(update_memo_sql, (classType, numType, q_id2))
                self.con.commit()
                print (classType)
            except:
                print(line)
                break
        f.close()

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    j.update_wh()