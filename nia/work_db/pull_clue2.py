#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-16
# 클루 (#8) 관련의 초안


import json
import logging
import os, sys
import random
import math
import time
import re
import concurrent.futures
import string
from multiprocessing import Pool

import pymysql

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('/home/msl/ys/cute'))
import custom_logger
# from morp_analyze_my import NLPAnalyzer


def return_myself(token):
    return token

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(custom_logger.MyHandler())
logger.info("Finish setting logger")


class SquadDb():

    def __init__(self):
        ###user_input#########################################################
        self.db_table = "MRC_TRAIN"
        self.data_output_dir = "/home/msl/ys/cute/nia/check"
        self.lang = "kor"
        self.version = "1"
        self.test_ratio = 0.1    # dev_ratio
        self.maximum = None
        self.is_divide = False
        self.is_dp = False
        self.is_random = True
        self.is_fixed = False
        #######################################################################

        self.db_cnf_dict = {}
        self.context_table = "(%s, %s, %s, %s, %s)"
        self.qna_table = "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.con = None
        self.cur = None
        self.random_end = "ORDER BY RAND()" if self.is_random else ""
        self.dp_end = "_dp" if self.is_dp else ""
        self.context_ori = ""
        # self.nlp_analyze = NLPAnalyzer()
        self.processed_ctx_list = list()

    def easy_mysql(self, cfg_dict, encoding='utf8', autocommit=False):
        self.con = pymysql.connect(host=cfg_dict['host'], user=cfg_dict['usr'],
                                   passwd=cfg_dict['pwd'], db=cfg_dict['db'], charset=encoding)
        self.cur = self.con.cursor()
        if autocommit is True:
            self.con.autocommit(True)

    def connect_db(self, table_name):
        try:        # try to connect to project db
            cfg_dict = dict(host='localhost', usr= 'root', pwd='data~secret!', db=table_name)
            self.easy_mysql(cfg_dict, encoding='utf8', autocommit=True)
            self.cur.execute("SET NAMES utf8")
        except Exception as e:
            logger.critical(e)
        logger.info("Finish connecting to database...")

    def db2squad2(self):
        with open('pull_clue2.json', 'r', encoding='utf-8') as f1:
            json_data1 = json.load(f1)
        fetch_sql_ctx = json_data1['data'][0]['yj']
        # fetch_sql_ctx = "select category_id, qa_id, question, answer, reason_morpheme from DATA_QA_TB WHERE category_id between 78435 and 84615"
        print (fetch_sql_ctx)
        self.cur.execute(fetch_sql_ctx)
        contexts = self.cur.fetchall()  # entire
        f2 = open("/home/msl/ys/cute/nia/check/yjchoi.txt", "w")
        logger.info("start..")

        for context in contexts:
            item = str(context[0]), str(context[1]), str(context[2]), str(context[3]), str(context[4])
            f2.write("\t".join(item))
            f2.write("\n")


if __name__ == "__main__":

    j = SquadDb()
    j.connect_db(j.db_table)
    j.db2squad2()
    logger.info("All finished")