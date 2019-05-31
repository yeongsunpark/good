author__ = "Lynn Hong"
__date__ = "06/08/2017"

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
import custom_logger
from morp_analyze_my import NLPAnalyzer


def return_myself(token):
    return token

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(custom_logger.MyHandler())
logger.info("Finish setting logger")

class SquadDb():

    def __init__(self):
        ###user_input#########################################################
        self.db_table = "SQUAD_NEWS_NIA"
        self.data_output_dir = "/home/msl/ys/cute/nia/check"
        self.version = "0500"
        self.test_ratio = 0.2    # dev_ratio (8:1:1로 나누기 위해)
        self.is_dp = False
        self.is_random = True
        self.mode = "clue"
        self.split = False
        #######################################################################


        self.db_cnf_dict = {}
        # self.context_table = "(%s, %s, %s, %s, %s)"
        # self.qna_table = "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.con = None
        self.cur = None
        self.random_end = "ORDER BY RAND()" if self.is_random else ""
        self.dp_end = "_dp" if self.is_dp else ""

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
        # fetch_sql_ctx = "SELECT id, title, context, context_morph, context_dp FROM all_context_all {};".format(self.random_end)
        if self.mode == "clue":
            fetch_sql_ctx = "SELECT id, title, context, source FROM all_context_error {};".format(self.random_end)
        elif self.mode == "no_answer":
            fetch_sql_ctx = "SELECT id, title, context, source FROM all_context_all where season=4 or season = 7 {};".format(
                self.random_end)
        else:
            fetch_sql_ctx = "SELECT id, title, context, source FROM all_context_all where season=1 or season=2 or season=3 or season=6 {};".format(self.random_end)
        # fetch_sql_ctx = "SELECT CTX.id, CTX.title, CTX.context  FROM all_context as CTX INNER JOIN all_qna as QA on QA.c_id = CTX.id WHERE CTX.season = 5 and QA.question IS NOT NULL AND QA.ANSWER IS NOT NULL GROUP BY CTX.id {} ".format(self.random_end)
        self.cur.execute(fetch_sql_ctx)
        contexts = self.cur.fetchall()   # entire

        contexts_not_fix = [c for c in contexts]  # not fix
        # contexts_not_fix = [c for c in contexts if c[0] not in contexts_dev_fix_ids]  # not fix
        logger.info("len(contexts): {}".format(len(contexts)))
        # logger.info("len(contexts_dev_fix_ids): {}".format(len(contexts_dev_fix_ids))) # 없지. 
        logger.info("len(contexts_not_fix): {}".format(len(contexts_not_fix)))  # 위에 것과 같아야함.

        if self.split :
            train_cnt = math.floor((len(contexts)) * (1 - self.test_ratio))
            context_train = random.sample(contexts_not_fix, train_cnt)  # 0.8은 여기
            c_dev_tmp1 = [c for c in contexts_not_fix if c not in context_train]  # 나머지는 여기
            # c_dev_tmp2 = list(contexts_dev_fix)  # 없음.
            logger.info("c_dev_tmp1: {}".format(len(c_dev_tmp1)))
            # logger.info("c_dev_tmp2: {}".format(len(c_dev_tmp2)))
            context_dNt = c_dev_tmp1  # 0.2는 여기 (그냥 한 번 더 넣을래)
            # context_dNt = c_dev_tmp1 + c_dev_tmp2  # 0.2는 여기
            dNt_cnt = math.floor((len(contexts) - len(context_train)) * 0.5)  # 전체 본문 길이 - train 본문(80%) 길이 / 2 -> 10%
            context_dev = random.sample(context_dNt, dNt_cnt)
            context_test = [c for c in contexts if c not in context_train and c not in context_dev]
            logger.info("train_cnt: {}".format(train_cnt))
            logger.info("Len context_train: {}".format(len(context_train)))
            logger.info("Len context_dev: {}".format(len(context_dev)))
            logger.info("Len context_test: {}".format(len(context_test)))
        else:
            context_all = contexts

        # for data_type in ["train", "dev", "test"]:
        for data_type in ["all"]:
            cnt = 0
            result = dict()
            result['version'] = self.version
            result['creator'] = "MINDs Lab."
            result['data'] = list()
            logger.info("Data type {} start..".format(data_type))
            for context in eval("context_{}".format(data_type)):
                data_dict = dict()      # each context
                data_dict['title'] = context[1]
                data_dict['source'] = context[3]
                data_dict['paragraphs'] = list()
                para_dict = dict()
                try:
                    para_dict['context'] = context[2]
                except IndexError:
                    logger.critical(context)
                    exit()

                qas_list = list()
                if self.mode == "clue":
                    fetch_sql_qa = "SELECT q_id, question, answer_start, answer, classType, reason, reason_start_index  FROM all_qna_error " \
                                    "WHERE c_id='{}'".format(context[0])
                elif self.mode == "no_answer":
                    fetch_sql_qa = "SELECT q_id, question, classType FROM all_qna " \
                                    "WHERE c_id='{}'".format(context[0])
                else:
                    fetch_sql_qa = "SELECT q_id, question, answer_start, answer, classType FROM all_qna " \
                                    "WHERE c_id='{}'".format(context[0])
                self.cur.execute(fetch_sql_qa)
                for row in self.cur.fetchall():
                    if self.mode == "clue":
                        qa = {'id': row[0], 'answers': [{'answer_start': row[2], 'text': row[3]}],
                              'question': row[1], 'classtype': row[4], 'clue':[{'clue_start': row[6], 'clue_text': row[5]}]}
                    elif self.mode == "no_answer":
                        qa = {'id': row[0], 'question': row[1], 'classtype': row[2]}
                    else:
                        qa = {'id': row[0], 'answers': [{'answer_start': row[2], 'text': row[3]}],
                                'question': row[1], 'classtype':row[4]}
                    qas_list.append(qa)
                    cnt += 1
                para_dict['qas'] = qas_list
                if qas_list == "":
                    continue
                else:
                    data_dict['paragraphs'].append(para_dict)
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
            logger.info("Data dump {} finished..: len {}".format(data_type, cnt))


if __name__ == "__main__":

    j = SquadDb()
    j.connect_db(j.db_table)
    j.db2squad()
    logger.info("All finished")