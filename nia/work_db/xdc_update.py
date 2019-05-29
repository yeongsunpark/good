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

    def update_data(self):
        cate_dict = {"정치": 1, "경제": 2, "사회": 3, "생활": 4, "IT/과학": 5, "연예": 6, "스포츠":7, "문화":8, "미용/건강":9}
        f = open("/home/msl/ys/cute/nia/xdc/season7_text_com.txt" ,"r")
        for line in f:
            item = self.line2item(line)

            id = item[0]
            context = item[1]
            cate = cate_dict[item[2]]

            try:
                update_memo_sql = "update all_context set source = %s where id = %s and context = %s"
                self.cur.execute(update_memo_sql, (cate, id, context))
                self.con.commit()
                print (item[0])
            except:
                print(line)
                break
        f.close()

    def update_wh(self):
        f = open("/home/msl/ys/cute/nia/xdc/0424_wh_com.txt" ,"r")
        for line in f:
            item = self.line2item(line)

            q_id = item[0]
            question = item[1]
            wh = [item[2]]

            try:
                update_memo_sql = "update all_qna set classType = %s where q_id = %s and question = %s"
                self.cur.execute(update_memo_sql, (wh, q_id, question))
                self.con.commit()
                print (item[0])
            except:
                print(line)
                break
        f.close()

    def update_startend(self):
        f = open("/home/msl/ys/cute/nia/sw2.txt")
        for line in f:
            item = self.line2item(line)
            q_id, answer_start, answer_end, answer = item[0], item[1], item[2], item[3]
            try:
                # update_start_sql = "update all_qna set answer_start = %s where q_id = %s and answer = %s"
                update_end_sql = "update all_qna set answer_end = %s where q_id = %s and answer = %s"
                # self.cur.execute(update_start_sql, (answer_start, q_id, answer))
                self.cur.execute(update_end_sql, (answer_end, q_id, answer))
                self.con.commit()
                print (q_id)
            except Exception as e:
                print (e)
                print (line)
                break
        f.close()

    def update_dup(self):
        f = open("/home/msl/ys/cute/nia/up_dup.tsv")
        for line in f:
            item = self.line2item(line)
            q_id, new_question = item[0], item[1]
            try:
                update_end_sql = "update all_qna set question = %s where q_id = %s"
                # self.cur.execute(update_start_sql, (answer_start, q_id, answer))
                self.cur.execute(update_end_sql, (new_question, q_id))
                self.con.commit()
                print (q_id)
            except Exception as e:
                print (e)
                print (line)
                break
        f.close()

    def update_source(self):
        fetch_sql_ctx = "select id, context from all_context_error where id >=108130"
        self.cur.execute(fetch_sql_ctx)
        contexts = self.cur.fetchall()   # entire

        for context in contexts:
            try:
                update_source = "update all_context_error set source = (select source from all_context where context = '{}' limit 1) "\
                                "where context = '{}' ".format(context[1], context[1])
                self.cur.execute(update_source)
                self.con.commit()
            except Exception as e:
                print (e)
                print (update_source)
                print (context[1])
                break

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    j.update_source()