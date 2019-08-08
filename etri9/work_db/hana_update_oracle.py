#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-07

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

#import pymysql
import cx_Oracle

sys.path.append(os.path.abspath('..'))
import custom_logger
from morp_analyze_my import NLPAnalyzer

os.environ["NLS_LANG"] = ".AL32UTF8"

def return_myself(token):
    return token

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(custom_logger.MyHandler())
logger.info("Finish setting logger")

class SquadDb():

    def __init__(self):
        ###user_input#########################################################
        self.db_table = "DBDNLP11"
        self.data_output_dir = "/maum/upload/mrc/hana_mrc_pre/data/output2"
        self.lang = "kor"
        self.version = "5"
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
        self.random_end = "order by DBMS_RANDOM.RANDOM" if self.is_random else ""
        self.dp_end = "_dp" if self.is_dp else ""
        self.context_ori = ""
        self.nlp_analyze = NLPAnalyzer()
        self.processed_ctx_list = list()

    def easy_mysql(self, cfg_dict, encoding='utf8', autocommit=False):
        #self.con = pymysql.connect(host=cfg_dict['host'], user=cfg_dict['usr'], passwd=cfg_dict['pwd'], db=cfg_dict['db'], charset=encoding)
        con_string = cfg_dict['usr'] + '/' +  cfg_dict['pwd'] + '@' + cfg_dict['host'] + ':' + '1543' + '/' + cfg_dict['db']
        self.con = cx_Oracle.connect(con_string)
        self.cur = self.con.cursor()
        if autocommit is True:
            self.con.autocommit(True)

    def connect_db(self, table_name):
        try:        # try to connect to project db
            #cfg_dict = dict(host=self.db_cnf_dict['host'], usr=self.db_cnf_dict['usr'],
            #                pwd=self.db_cnf_dict['pwd'], db=self.db_cnf_dict['db'])
            ##cfg_dict = dict(host='localhost', usr= 'root', pwd='data~secret!', db=table_name)
            cfg_dict = dict(host='10.60.73.21', usr='NLPCON', pwd='kebhana1!', db=table_name)
            #self.cfg_dict = cfg_dict
            #self.easy_mysql(cfg_dict, encoding=self.db_cnf_dict['encoding'], autocommit=True)     # turn-on autocummit, be careful!
            self.easy_mysql(cfg_dict, encoding='utf8', autocommit=True)
            self.cur.execute("SET NAMES utf8")
        except Exception as e:
            logger.critical(e)
        logger.info("Finish connecting to database...")

    def update_data(self):
        header = True
        f = open("/home/msl/ys/cute/data/title_replace.txt", "r")
        try:
            for data in f:
                if header:
                    header = False
                    continue
                item = data.replace("\n","").split("\t")
                old_title = item[0]
                new_title = item[1]
                update_sql = "UPDATE nlpadm.mlt_mrc_all_context SET context_dp = %s WHERE title = %s"
                self.cur.execute(update_sql, (new_title, old_title))
                self.con.commit()
        except:
            logger.error("no select_data")

    def replace_data(self):
        try:
            update_sql = "UPDATE nlpadm.mlt_mrc_all_context SET title = replace(title, '<br>', '') WHERE title LIKE '%<br>'"
            self.cur.execute(update_sql)
            self.con.commit()
        except:
            logger.error("no select_data")


if __name__ == "__main__":

    j = SquadDb()
    j.connect_db(j.db_table)
    j.replace_data()
    logger.info("All finished")