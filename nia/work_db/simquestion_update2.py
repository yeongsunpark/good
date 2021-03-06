#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-23

import logging
import os, sys
import pymysql
sys.path.append(os.path.abspath('..'))
# import custom_logger
import csv

class SquadDb():

    def __init__(self):
        self.db_cnf_dict = {"host": '10.122.64.83', "usr": "root", "pwd": "data~secret!",
                            "db": "SQUAD_NEWS_NIA", "encoding": "utf8"}
        self.con = None
        self.cur = None
        self.connect_db()

    def easy_mysql(self, cfg_dict, encoding='utf8', autocommit=False):
        self.con = pymysql.connect(host=cfg_dict['host'], user=cfg_dict['usr'],
                                   passwd=cfg_dict['pwd'], db=cfg_dict['db'], charset=encoding)
        self.cur = self.con.cursor()
        if autocommit is True:
            self.con.autocommit(True)

    def connect_db(self):
        try:        # try to connect to project db
            cfg_dict = dict(host=self.db_cnf_dict['host'], usr=self.db_cnf_dict['usr'],
                            pwd=self.db_cnf_dict['pwd'], db=self.db_cnf_dict['db'])
            self.easy_mysql(cfg_dict, encoding=self.db_cnf_dict['encoding'], autocommit=True)     # turn-on autocummit, be careful!
            self.cur.execute("SET NAMES utf8")
            print ("hi")
        except Exception as e:
            pass
    def update_data(self):
        cate_dict = {"정치": 1, "경제": 2, "사회": 3, "생활": 4, "IT/과학": 5, "연예": 6, "스포츠":7, "문화":8, "미용/건강":9}
        f = open("/home/msl/ys/cute/nia/sim/유사질문 생성 시트 - 전효진_2.tsv" ,"r")
        for line in f:
            line = line.replace("\n","")
            item = line.split("\t")

            c_id = item[0]
            q_id = item[1]
            question = item[2]
            # print (question)
            s_question = item[3]
            answer = item[4]
            clue = item[5]

            if question != s_question:
                try:
                    insert_sql = "insert into `all_qna_error` (c_id, q_id, question, answer_start, answer_end, answer, numType, classType, isFlexible, reason, reason_start_index, reason_end_index) " \
                                 "select c_id, concat(substring_index(q_id,'-',1), '-2'), %s, answer_start, answer_end, answer, numType, classType, isFlexible, reason, reason_start_index, reason_end_index " \
                                 "from `all_qna_error` where c_id = %s and q_id = %s"
                                 # "from `all_qna_error` where question = %s and answer = %s and c_id = %s and q_id = %s and reason = %s"
                    self.cur.execute(insert_sql, (s_question, c_id, q_id))
                    # self.cur.execute(insert_sql, (s_question, question, answer, c_id, q_id, clue))
                    self.con.commit()
                    # print (item[0])
                except:
                    pass
                    # print (item)
                    # break

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db()
    j.update_data()