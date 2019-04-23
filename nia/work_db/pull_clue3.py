#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-16

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
            #cfg_dict = dict(host=self.db_cnf_dict['host'], usr=self.db_cnf_dict['usr'],
            #                pwd=self.db_cnf_dict['pwd'], db=self.db_cnf_dict['db'])
            cfg_dict = dict(host='localhost', usr= 'root', pwd='data~secret!', db=table_name)
            #self.cfg_dict = cfg_dict
            #self.easy_mysql(cfg_dict, encoding=self.db_cnf_dict['encoding'], autocommit=True)     # turn-on autocummit, be careful!
            self.easy_mysql(cfg_dict, encoding='utf8', autocommit=True)
            self.cur.execute("SET NAMES utf8")
        except Exception as e:
            logger.critical(e)
        logger.info("Finish connecting to database...")

    def db2squad(self):
        data_type = "real"
        fetch_sql_ctx = "SELECT category_id, text, context_id FROM DATA_CONTEXT_TB WHERE status='CM' limit 10"
        self.cur.execute(fetch_sql_ctx)
        contexts = self.cur.fetchall()   # entire
        cnt = 0
        result = dict()
        result['version'] = self.version
        result['creator'] = "MINDs Lab."
        result['data'] = list()

        logger.info("start..")

        for context in contexts:
            qas_list = list()
            fetch_sql_qa = "SELECT category_id, qa_id, question, answer, start_index, end_index, reason_morpheme, reason_start_index, reason_end_index, class_type " \
                           "FROM DATA_QA_TB WHERE category_id='{}' and class_type is not null".format(context[0])
            self.cur.execute(fetch_sql_qa)
            # print (fetch_sql_qa)

            for row in self.cur.fetchall():
                if row[2] is not None and row[3] is not None and row[6] is not None and row[9] is not None:
                # if row[0:10] is not None:
                    print (row)
                    qa = {'q_id': str(row[0]) + "_" + str(row[1]), 'answers': row[3], 'start_index': row[4],
                          'end_index': row[5], 'question': row[2],
                          'reason': row[6], 'reason_start': row[7], "reason_end": row[8], "wh": row[9]}
                    qas_list.append(qa)
                    cnt += 1

            # para_dict['main_qa_list'] = qas_list
            # print (context)
            data_dict = dict()  # each context
            data_dict['seq'] = context[0]
            data_dict['main_qa_list'] = list()
            data_dict['text'] = context[1]
            # fileName = context[0]
            # source = 0
            # seq = ""
            # doc_type = 0
            data_dict['main_qa_list'] = qas_list
            # data_dict['paragraphs'].append(para_dict)
            result['data'].append(data_dict)

        logger.info("Finish creating json structure({})".format(data_type))
        with open(os.path.join(self.data_output_dir, "ko_nia_v{}_squad{}_{}.json".
                format(self.version, self.dp_end, data_type)),
                  'w', encoding='utf8') as fp:
            json.dump(result, fp, ensure_ascii=False)
        with open(os.path.join(self.data_output_dir, "ko_nia_v{}_squad_pretty{}_{}.json".
                format(self.version, self.dp_end, data_type)),
                  'w', encoding='utf8') as fp:
            json.dump(result, fp, ensure_ascii=False, indent=2)
        logger.info("Data dump {} finished..:".format(cnt))

if __name__ == "__main__":

    j = SquadDb()
    j.connect_db(j.db_table)
    j.db2squad()
    logger.info("All finished")