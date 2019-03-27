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

        self.is_divide = False  # for squad2db, db2squad
        self.context_table = "(%s, %s, %s, %s, %s)"
        self.qna_table = "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.con = None
        self.cur = None
        self.context_ori = ""

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

    def insert_mysql(self, sql, varTuple):
        try:
            self.cur.execute(sql, varTuple)
            logger.debug("Data inserted")
        except pymysql.Error as e:
            logger.critical(e)
            logger.critical(sql%varTuple)
            exit()

    def insert_data(self, table, value_part, var_tuple, morph_end):
        if "context" in table:
            sql = "INSERT INTO {}(id, season, data_type, title, context{}) VALUES {}".\
                format(table, morph_end, value_part)
        else:
            sql = "INSERT INTO {}(c_id, q_id, question{}, answer_start{}, answer_end{}, answer{}, cate1, cate2, cate3) VALUES {}".\
                format(table, morph_end, morph_end, morph_end, morph_end, value_part)
        self.insert_mysql(sql, var_tuple)

    def squad2db(self, json_location, start_id, season, data_type, table_name):
        self.connect_db(table_name)
        with open(json_location) as f:
            data = json.load(f)
        data = data['data']
        if start_id is None:
            start_id = 1
        for d in data:
            try:
                logger.info(d['title'])
                title = d['title']
            except KeyError:
                continue
            for para in d['paragraphs']:
                q_context = str(para['context'])
                try:
                    self.context_ori = str(para['context_ori'])
                except KeyError:
                    if self.context_ori == "":
                        exit("There's no context_ori")
                var_tuple_ctx = (start_id, season, data_type, title.strip(), q_context.strip())
                var_tuple_ctx_ori = (start_id, season, data_type, title.strip(), self.context_ori.strip())
                self.insert_data(table="all_context", value_part=self.context_table, var_tuple=var_tuple_ctx, morph_end="")
                self.insert_data(table="all_context_ori", value_part=self.context_table, var_tuple=var_tuple_ctx_ori, morph_end="")
                for qa in para['qas']:
                    q = str(qa['question'])
                    q_id = qa['id']
                    for a in qa['answers']:
                        a_start = a['answer_start']   # int
                        try:
                            a_end = a['answer_end']   # int
                        except KeyError:
                            a_end = -1
                        text = a['text']  # answer text
                        var_tuple_qa = (start_id, q_id, q.strip().strip("?").strip(), a_start, a_end, text.strip(),
                                        '', '', '')
                    self.insert_data(table="all_qna", value_part=self.qna_table, var_tuple=var_tuple_qa, morph_end="")
                start_id += 1
            logger.debug("num of para: %i" % len(d['paragraphs']))

re_quotation = re.compile(r"\[+[\"\'](\[\[.+\]\])[\"\']\]+")


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

    if mode == "squad2db":
        j.squad2db(json_input, int(start_id), season, data_type, db_table)
    logger.info("All finished")
