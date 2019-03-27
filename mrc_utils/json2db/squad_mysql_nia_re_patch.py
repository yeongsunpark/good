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

    def extract_passage(self, ctx, answer, location, c_id, q_id):
        sentence_list = list()
        is_skip = False
        logger.info(answer)
        processed_ans = self.nlp_analyze.get_tree_result(answer)   # list
        # [[['이것/np', 'ㄴ/jx'], ['정답/nng', '이/vcp', '다/ec']]] # [[['정답/nng']]]
        logger.debug(processed_ans)
        processed_ans_plain, depth = self.make_plain_list(processed_ans)
        processed_ans_plain = ['|/sw'] * 5 + processed_ans_plain + ['|/sw'] * 5    # plain list
        if depth == 2:
            processed_ans = [processed_ans]
        logger.debug("processed_ans: {}".format(processed_ans))
        logger.debug("processed_ans_plain: {}".format(processed_ans_plain))
        ctx = "{}{}{}{}{}".format(ctx[:location], "|"*5, ctx[location:location+len(answer)], "|"*5, ctx[location+len(answer):])
        processed_txt, sentence_list = self.nlp_analyze.get_tree_result(ctx, sentence_list=True)
        logger.debug(processed_txt)
        processed_txt_plain, depth = self.make_plain_list(processed_txt)    # plain list
        if depth == 2:
            processed_txt = [processed_txt]

        logger.debug("processed_ans: {}".format(processed_ans))
        logger.debug("processed_ans_plain: {}".format(processed_ans_plain))
        logger.debug("processed_txt: {}".format(processed_txt))
        logger.debug("processed_txt_plain: {}".format(processed_txt_plain))
        marker_idxes = [(j, j + 5) for j in range(len(processed_txt_plain))
                        if processed_txt_plain[j:j + 5] == ['|/sw'] * 5]
        logger.debug(marker_idxes)
        if len(marker_idxes) % 2 == 0:
            if len(marker_idxes) == 2:
                start_idx = marker_idxes[0][0]
                end_idx = marker_idxes[1][1] - 10
            else:
                logger.critical("Not 2 markers...({}) skip: {}".format(len(marker_idxes), q_id))
                is_skip = True
                return 0, 0, 0, 0, is_skip
        else:
            logger.critical("Not 2 markers...({}) skip: {}".format(len(marker_idxes), q_id))
            is_skip = True
            return 0, 0, 0, 0, is_skip

        logger.debug("start_idx: {}".format(start_idx))
        logger.debug("end_idx: {}".format(end_idx))
        for k in range(len(processed_txt)):  # sentence
            for l in range(len(processed_txt[k])):  # token
                logger.debug(processed_txt[k][l])
                tmp_idxes = [(j, j + 5) for j in range(len(processed_txt[k][l]))
                                if processed_txt[k][l][j:j + 5] == ['|/sw'] * 5]
                if len(tmp_idxes) != 0:
                    logger.debug(tmp_idxes)
                    new_processed_txt = self.remove_list_sequence(processed_txt[k][l], tmp_idxes)
                    logger.debug(new_processed_txt)
                    processed_txt[k][l] = new_processed_txt
                    #processed_txt[k][l] = list(filter('|/sw'.__ne__, processed_txt[k][l]))
                    logger.debug(processed_txt[k][l])
        logger.debug(processed_txt)
        final_answer = list()
        cnt = 0
        for k in range(len(processed_txt)):
            tmp = list()
            for l in range(len(processed_txt[k])):
                tmp2 = list()
                for m in range(len(processed_txt[k][l])):   # morph
                    if cnt >= start_idx and cnt < end_idx:
                        logger.debug(processed_txt[k][l][m])
                        tmp2.append(processed_txt[k][l][m])
                    cnt += 1
                if len(tmp2) > 0:
                    tmp.append(tmp2)
            if len(tmp) > 0:
                final_answer.append(tmp)
        processed_txt_plain = self.remove_list_sequence(processed_txt_plain, marker_idxes)
        #processed_txt_plain = list(filter('|/sw'.__ne__, processed_txt_plain))
        final_answer_plain, depth = self.make_plain_list(final_answer)
        try:
            assert (processed_txt_plain[start_idx:end_idx] == final_answer_plain)
        except AssertionError:
            logger.error("{} != {}".format(processed_txt_plain[start_idx:end_idx],
                                           final_answer_plain))
            is_skip = True
            return 0, 0, 0, 0, is_skip
        logger.debug("answer_processed: {}".format(processed_txt_plain[start_idx:end_idx]))
        logger.debug("answer_processed_return: {}".format(final_answer))
        logger.debug(str(processed_txt))
        return start_idx, end_idx, str(processed_txt), str(final_answer), is_skip, sentence_list

    def remove_list_sequence(self, input_list, marker_idxes):
        logger.debug(input_list)
        logger.debug(marker_idxes)
        new_ptp = list()
        if len(marker_idxes) > 1:
            for i in range(len(marker_idxes)):
                if i == 0:
                    new_ptp += input_list[:marker_idxes[i][0]]
                    new_ptp += input_list[marker_idxes[i][1]:marker_idxes[i+1][0]]
                    logger.debug(input_list[:marker_idxes[i][0]])
                else:
                    new_ptp += input_list[marker_idxes[i][1]:]
                    logger.debug(input_list[marker_idxes[i][1]:])
        else:
            new_ptp += input_list[:marker_idxes[0][0]]
            new_ptp += input_list[marker_idxes[0][1]:]
        logger.debug(new_ptp)
        return new_ptp

    def process_qa(self, type, season, table_name):
        db_cnf_dict = {"host": 'localhost', "usr": "root", "pwd": "data~secret!", "db": table_name, "encoding": "utf8"}
        self.connect_db(table_name)
        if type == "re_patch":
            with open("/home/msl/ys/cute/nia/check/re_patch_all.txt") as f:  # 바꿔줌
                qas = f.readlines()
        else:
            logger.error("You select the wrong type({}). Please re-check your command".format(type))
            exit()

        workers = 20 # 20 으로 바꿈
        r = 300 # 오류나서 300 을 200 으로 줄임

        if type == "re_patch":
            # re_patch(table_name, qas, 0, r) # 위 r 의 수를 re_patch 해서 나온 오류 개수 만큼 늘려줘야함.
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(re_patch, table_name, qas, n, r) for n in range(0, len(qas), r)}

def re_patch(table_name, qas, n, r):
    exec("j{} = SquadDb()".format(n))
    print("j{} = SquadDb()".format(n))
    eval("j{}.connect_db('{}')".format(n, table_name))
    logger.info("Finish connecting to database...: {}".format(n))

    logger.info("processing: {} ..< {}".format(n, n + r))
    for q_line in qas[n:n+r]:
        item = q_line.strip().split("\t")
        fetch_sql = "select q.c_id, q.q_id, q.answer, q.answer_start, c.context from all_qna q, all_context c " \
                    "where q.c_id = %s AND q.q_id = %s AND q.c_id = c.id;"
        eval("j{}".format(n)).cur.execute(fetch_sql, (item[0], item[1]))
        q = eval("j{}".format(n)).cur.fetchone()
        # q: c_id, q_id, answer, answer_start, context
        c_id = q[0]; q_id = q[1]; answer = q[2]; answer_s = q[3]; ctx = q[4]
        new_s, new_e, new_ctx, new_ans, is_skip, sentence_list = \
            eval("j{}".format(n)).extract_passage(ctx, answer, answer_s, c_id, q_id)
        sql = "INSERT INTO all_context_diff VALUE(%s, %s, %s);"

        sql_diff = "SELECT u_id FROM all_context_diff WHERE depend_id = %s ORDER BY u_id DESC LIMIT 1;"
        eval("j{}".format(n)).cur.execute(sql_diff, c_id)
        uu = eval("j{}".format(n)).cur.fetchone()
        if uu is None:
            u_id = 1
        else:
            u_id = uu[0] + 1

        eval("j{}".format(n)).cur.execute(sql, (c_id, u_id, new_ctx))
        logger.info("Insert new c: {}-{}".format(c_id, u_id))
        sql = "UPDATE all_qna SET c_id = %s WHERE c_id = %s AND q_id = %s;"
        eval("j{}".format(n)).cur.execute(sql, ("{}-{}".format(c_id, u_id), c_id, q_id))
        eval("j{}".format(n)).cur.execute(sql, ("{}-{}".format(c_id, u_id), c_id, "{}2".format(q_id[:-1])))
        logger.info("Update q: {}".format(q_id))
        logger.debug(new_ans)

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

    if mode == "re_patch":
        j.process_qa('re_patch', season, db_table)
    logger.info("All finished")