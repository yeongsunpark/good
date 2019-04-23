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
        self.context_table = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
            sql = "INSERT INTO {}(id, season, data_type, title, context{}, source, doc_type, sub_doc_type, fileName, seq) VALUES {}".\
                format(table, morph_end, value_part)
        else:
            sql = "INSERT INTO {}(c_id, q_id, question{}, answer_start{}, answer_end{}, answer{}, numType, classType, isFlexible) VALUES {}".\
                format(table, morph_end, morph_end, morph_end, morph_end, value_part)
        self.insert_mysql(sql, var_tuple)

    def squad2db(self, json_location, start_id, season, data_type, table_name, q_id_index):
        self.connect_db(table_name)
        with open(json_location) as f:
            data = json.load(f)
        data = data['data']
        if start_id is None:
            start_id = 1
        for d in data:
            try:
                logger.info(d['fileName'])
                title = d['seq']
                fileName = d['fileName']
                sub_doc_type = d['sub_doc_type']
                seq = d['seq']
                doc_type = d['doc_type']
                source = d['source']
                q_context = d['text']
                # logger.info(q_context)

                ### var_tuple_ctx = (start_id, season, data_type, str(title).strip(), q_context.strip(), source, doc_type, sub_doc_type, fileName, seq)
                var_tuple_ctx = (start_id, season, data_type, str(title).strip(), q_context, source, doc_type, sub_doc_type, fileName, seq)

                # var_tuple_ctx_ori = (start_id, season, data_type, title.strip(), self.context_ori.strip())
                self.insert_data(table="all_context", value_part=self.context_table, var_tuple=var_tuple_ctx, morph_end="")
                # self.insert_data(table="all_context_ori", value_part=self.context_table, var_tuple=var_tuple_ctx_ori, morph_end="")
            except KeyError:
                exit("something wrong")

            # for qa in zip (d['main_qa_list']):
            for qa, i in zip (d['main_qa_list'], range(len(d['main_qa_list']))):
                answer = qa['answer']
                begin = qa['begin']
                q = str(qa['question'])
                isf = qa['isFlexible']
                end = qa['end']
                numType = qa['type']
                classType = qa['classType']
                q_id = creator + "_" + str(q_id_index) + "-1"
                ### var_tuple_qa = (start_id, q_id, q.strip(), begin, end, answer.strip(), numType, classType, isf) # q_id 를 i+1 로 표현해서 본문 시작할 때마다 1로 했다가 바꿈!
                var_tuple_qa = (start_id, q_id, q.strip(), begin, end, answer, numType, classType, isf) # q_id 를 i+1 로 표현해서 본문 시작할 때마다 1로 했다가 바꿈!
                self.insert_data(table="all_qna", value_part=self.qna_table, var_tuple=var_tuple_qa, morph_end="")
                q_id_index +=1
            start_id += 1
        # logger.debug("num of para: %i" % len(d['paragraphs']))

re_quotation = re.compile(r"\[+[\"\'](\[\[.+\]\])[\"\']\]+")


if __name__ == "__main__":

    try:
        """
        mode = sys.argv[1]
        season = sys.argv[2]
        db_table = sys.argv[3]
        json_input = sys.argv[4]
        start_id = sys.argv[5] # 1
        data_type = sys.argv[6] # news
        q_id_index = sys.argv[7] # 수정하기! (1)
        """
        mode = "squad2db"
        season = "6"  # 수정하기!
        db_table = "SQUAD_NEWS_NIA"
        json_input = "/home/msl/ys/cute/nia/common_tsv/didi4_0423.json"
        start_id = 79376  # 수정하기! 1(context_id)
        data_type = "news"
        creator = "m5"  # 수정하기!
        q_id_index = 305721  # 수정하기! (1)(q_id)
        #  select max(abs(substring_index(substring_index(q_id, "_",-1), "-",1))) from all_qna; 이거에 +1 하기!
        # select count(*) from all_qna 이거에 +1 해도 똑같네 ㅋㅋㅋ
    except: print("")

    j = SquadDb()
    j.connect_db(db_table)

    if mode == "squad2db":
        j.squad2db(json_input, int(start_id), season, data_type, db_table, q_id_index)
    logger.info("All finished")
