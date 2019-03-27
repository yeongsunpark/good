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

        self.maximum = None  # for squad2db, db2squad
        self.is_divide = False  # for squad2db, db2squad
        self.is_dp = False
        self.db_cnf_dict = {}
        # self.context_table = "(%s, %s, %s, %s, %s, %s)"
        self.context_table = "(%s, %s, %s, %s, %s)"
        self.qna_table = "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.con = None
        self.cur = None
        self.dp_end = "_dp" if self.is_dp else ""
        self.context_ori = ""
        self.nlp_analyze = NLPAnalyzer()
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
            #self.easy_mysql(cfg_dict, encoding=self.db_cnf_dict['encoding'], autocommit=True)     # turn-on autocummit, be careful!
            self.easy_mysql(cfg_dict, encoding='utf8', autocommit=True)
            self.cur.execute("SET NAMES utf8")
        except Exception as e:
            logger.critical(e)
        logger.info("Finish connecting to database...")

    def insert_mysql(self, sql, varTuple):
        try:
            self.cur.execute(sql, varTuple)
            logger.debug("Data inserted")
        except pymysql.Error as e:
            logger.critical(e)
            logger.critical(sql%varTuple)
            exit()

    def check_data(self, season):
        workers = 30
        r = 300
        fetch_sql = "SELECT c_id, q_id, question_morph, answer_morph, answer_start_morph, answer_end_morph, c.context_morph " \
                    "FROM all_context_all c, all_qna q WHERE c.id=q.c_id AND q.q_id LIKE '{}_%-1' " \
                    "ORDER BY cast(c_id as unsigned), q_id;".format(season)
        self.cur.execute(fetch_sql)
        qas = self.cur.fetchall()
        logger.info("Fetch all qns data finished")
        #check_index(qas, 0, r)
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
            fs = {exe.submit(check_index, qas, n, r) for n in range(0, len(qas), r)}

    def make_plain_list(self, input_list):
        return_list = list()
        depth = 0
        for x in input_list:    # x: sentence
            for y in x:     # y: token
                if type(y) != list:
                    return_list.append(y)
                    depth = 2
                else:
                    for z in y:     # z: morph
                        return_list.append(z)
                        depth = 3
        return return_list, depth

re_quotation = re.compile(r"\[+[\"\'](\[\[.+\]\])[\"\']\]+")

def check_index(qas, n, r):
    exec("j{} = SquadDb()".format(n))
    return_list = list()
    logger.info("processing: {} ..< {}".format(n, n + r))
    for q in qas[n:n+r]:
        ctx_plain, depth = eval("j{}".format(n)).make_plain_list(eval(q[6]))
        answer_plain, depth = eval("j{}".format(n)).make_plain_list(eval(q[3]))
        try:
            assert (ctx_plain[q[4]:q[5]] == answer_plain)
        except AssertionError:
            return_list.append("{}\t{}\t{}\t{}".format(q[0], q[1], ctx_plain[q[4]:q[5]], answer_plain))
            # c_id, q_id, 본문에서 답변의 위치 뽑은 것, 제대로된 답변(버티컬 바 안의 답변)
            # q[4]는 answer_start_morph 고 q[5]는 answer_end_morph 다.
    if len(return_list) != 0:
        with open("check/re_patch_{}.txt".format(n), "a") as f:
            f.write("\n".join(return_list))
            f.write("\n")


if __name__ == "__main__":

    try:
        mode = sys.argv[1]
        season = sys.argv[2]
        db_table = sys.argv[3]
        json_input = sys.argv[4]
        start_id = sys.argv[5]
        data_type = sys.argv[6]
    except: print("")

    j = SquadDb()
    j.connect_db(db_table)

    if mode == "check_data":
        j.check_data(season)
    logger.info("All finished")
