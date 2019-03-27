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

    def process_qa(self, type, season, table_name):
        db_cnf_dict = {"host": 'localhost', "usr": "root", "pwd": "data~secret!", "db": table_name, "encoding": "utf8"}
        self.connect_db(table_name)
        if type == "q_only":
            fetch_sql = "SELECT c_id, q_id, question FROM all_qna q " \
                        "WHERE q_id LIKE '%-2' AND question_morph IS NULL AND q_id LIKE '{}_%'" \
                        "ORDER BY cast(c_id as unsigned), q_id;".format(season)
        else:
            logger.error("You select the wrong type({}). Please re-check your command".format(type))
            exit()

        if type != "re_patch":
            self.cur.execute(fetch_sql)
            qas = self.cur.fetchall()
            logger.info("len of qas: {}".format(len(qas)))
        workers = 20 # 20 으로 바꿈
        r = 300 # 오류나서 300 을 200 으로 줄임

        if type == "q_only":
            #update_set_q(table_name, qas, 0, r)
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(update_set_q, table_name, qas, n, r) for n in range(0, len(qas), r)}

re_quotation = re.compile(r"\[+[\"\'](\[\[.+\]\])[\"\']\]+")

def update_set_q(table_name, qas, n, r):
    exec("j{} = SquadDb()".format(n))
    print("j{} = SquadDb()".format(n))
    eval("j{}.connect_db('{}')".format(n, table_name))
    logger.info("Finish connecting to database...: {}".format(n))

    logger.info("processing: {} ..< {}".format(n, n + r))
    for q in qas[n:n+r]:
        question = q[2]
        question_list = eval("j{}".format(n)).nlp_analyze.get_tree_result(question)
        logger.debug(question_list)
        fetch_sql = "SELECT answer_morph, answer_start_morph, answer_end_morph FROM all_qna " \
                    "WHERE c_id = %s AND q_id = %s;"
        eval("j{}".format(n)).cur.execute(fetch_sql, [q[0], "{}1".format(q[1][:-1])]) # fetch '-1' info
        original = eval("j{}".format(n)).cur.fetchone()
        logger.debug(original)

        update_sql = "UPDATE all_qna SET question_morph = %s, answer_morph = %s, " \
                    "answer_start_morph = %s, answer_end_morph = %s " \
                    "WHERE c_id = %s AND q_id = %s;"
        val_tuple = (str(question_list), original[0], original[1], original[2], q[0], q[1])
        logger.debug(val_tuple)
        eval("j{}".format(n)).cur.execute(update_sql, val_tuple)

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

    if mode == "q_only":
        j.process_qa('q_only', season, db_table)
    logger.info("All finished")
