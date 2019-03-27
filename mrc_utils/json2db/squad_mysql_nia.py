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

    def insert_data(self, table, value_part, var_tuple, morph_end):
        if "context" in table:
            #sql = "INSERT INTO {}(id, season, data_type, title, context{}, c_datetime) VALUES {}".\
            sql = "INSERT INTO {}(id, season, data_type, title, context{}) VALUES {}".\
                format(table, morph_end, value_part)
        else:
            sql = "INSERT INTO {}(c_id, q_id, question{}, answer_start{}, answer_end{}, answer{}, cate1, cate2, cate3) VALUES {}".\
                format(table, morph_end, morph_end, morph_end, morph_end, value_part)
        self.insert_mysql(sql, var_tuple)

    def fetch_text(self):
        #sql = "SELECT c.id, c.title, c.context, q.question, q.answer, c.c_datetime " \
        sql = "SELECT c.id, c.title, c.context, q.question, q.answer " \
              "FROM all_context c, all_qna q WHERE q.c_id=c.id AND q.q_id = '{}';"
        final_list = list()
        with open(os.path.join(self.data_root_dir, self.correction_data), "r") as f:
            for line in f:
                item = line.strip().split("\t")
                self.cur.execute(sql.format(item[0]))
                row = self.cur.fetchone()
                new_list = [str(x) for x in item + list(row)]
                final_list.append("\t".join(new_list))
        with open(os.path.join(self.data_root_dir,
                               "{}_original.tsv".format(self.correction_data.split(".")[0])),
                  "w") as f2:
            f2.write("\n".join(final_list))

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
                # c_datetime = d['c_datetime']
            except KeyError:
                continue
            for para in d['paragraphs']:
                if self.is_divide:
                    if random.random() >= self.test_ratio:
                        data_type = "train"
                    else:
                        data_type = "dev"
                q_context = str(para['context'])
                try:
                    self.context_ori = str(para['context_ori'])
                except KeyError:
                    if self.context_ori == "":
                        exit("There's no context_ori")
                # var_tuple_ctx = (start_id, season, data_type, title.strip(), q_context.strip(), c_datetime)
                var_tuple_ctx = (start_id, season, data_type, title.strip(), q_context.strip())
                #var_tuple_ctx_ori = (start_id, season, data_type, title.strip(), self.context_ori.strip(),c_datetime)
                var_tuple_ctx_ori = (start_id, season, data_type, title.strip(), self.context_ori.strip())
                self.insert_data(table="all_context", value_part=self.context_table, var_tuple=var_tuple_ctx, morph_end="")
                self.insert_data(table="all_context_ori", value_part=self.context_table, var_tuple=var_tuple_ctx_ori, morph_end="")
                if self.is_divide:
                    self.insert_data(table="{}_context".format(data_type), value_part=self.context_table, var_tuple=var_tuple_ctx, morph_end="")
                    self.insert_data(table="{}_context_ori".format(data_type), value_part=self.context_table, var_tuple=var_tuple_ctx_ori, morph_end="")
                for qa in para['qas']:
                    q = str(qa['question'])
                    q_id = qa['id']
                    # cates = qa['category'].split("-")
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

    def update_devset(self):
        dev_id_list = list()
        header = True
        with open(self.test_id_file) as f:
            for line in f:
                if header:
                    header = False
                    continue
                # lv.1 lv.2 category q_id question answer
                item = line.strip().split("\t")
                dev_id_list.append(item[3])
        logger.info("Len of dev_id_list: {}".format(len(dev_id_list)))

        fetch_sql_q = "SELECT c_id, q_id FROM all_qna WHERE q_id IN %s;"
        logger.debug(tuple(dev_id_list))
        self.cur.execute(fetch_sql_q, (tuple(dev_id_list),))
        test_rows = self.cur.fetchall()
        logger.info("Len of test_rows: {}".format(len(test_rows)))

        dev_ctx_id_list = list()
        dev_update_q = "UPDATE all_qna SET is_fixed = 1 WHERE q_id = %s;"
        for test_row in test_rows:
            logger.debug("test_row[1]: {}".format(test_row[1]))
            self.cur.execute(dev_update_q, (test_row[1],))  # update dev questions
            dev_ctx_id_list.append(test_row[0])

        insert_dev_ctx = "INSERT INTO dev_context_fix SELECT * FROM all_context_all WHERE id IN %s;"
        self.cur.execute(insert_dev_ctx, (tuple(dev_ctx_id_list),))

        insert_dev_q = "INSERT INTO dev_qna_fix SELECT * FROM all_qna " \
                        "WHERE q_id IN (SELECT q_id FROM all_qna WHERE c_id IN %s);"
        self.cur.execute(insert_dev_q, (tuple(dev_ctx_id_list),))

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

    def extract_passage(self, ctx, answer, location, c_id, q_id):
        sentence_list = list()
        is_skip = False
        logger.info(answer)
        processed_ans = self.nlp_analyze.get_tree_result(answer)   # list
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
        if type == "q_only":
            fetch_sql = "SELECT c_id, q_id, question FROM all_qna q " \
                        "WHERE q_id LIKE '%-2' AND question_morph IS NULL AND q_id LIKE '{}_%'" \
                        "ORDER BY cast(c_id as unsigned), q_id;".format(season)
        elif type == "check_dp_length":
            fetch_sql = "SELECT id, context, context_morph, context_dp " \
                        "FROM all_context_all c ORDER BY id;"
        elif type == "dp":
            fetch_sql = "SELECT id, context FROM all_context " \
                        "WHERE context_dp IS NULL AND cast(id AS unsigned) >= {} ORDER BY id;".format(self.start_id)
        elif type == "dp_q":
            fetch_sql = "SELECT c_id, q_id, question FROM all_qna " \
                        "WHERE question_dp IS NULL ORDER BY c_id, q_id;"
        elif type == "patch":
            #fetch_sql = "select c_id, q_id, answer, answer_start, context, context_morph from all_qna q, all_context c " \
            #            "where q.q_id LIKE '%-1' AND q.c_id = c.id ORDER BY c_id, q_id;"
            fetch_sql = "SELECT c_id, q_id, answer, answer_start, context " \
                        "FROM (SELECT * FROM all_context_all WHERE context LIKE '%|%') t, all_qna q " \
                        "WHERE t.id = q.c_id " \
                        "ORDER BY c_id, q_id;"
        elif type == "re_patch":
            with open("check/re_patch_all.txt") as f:  # 바꿔줌
                qas = f.readlines()
        elif type == "context":
            # process only data created at certain season
            fetch_sql = "select c_id, q_id, question, answer, answer_start, context from all_qna q, all_context c " \
                        "where q.q_id LIKE '%-1' AND q.q_id LIKE '{}_%' AND q.c_id = c.id AND question_morph is NULL and c.id> 0 " \
                        "ORDER BY CAST(c_id AS UNSIGNED), q_id;".format(season)
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
        elif type == "dp":
            #get_dp_multi("context", self.db_cnf_dict, qas, 0, len(qas))
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(get_dp_multi, "context", self.db_cnf_dict, qas, n, r) for n in range(0, len(qas), r)}
        elif type == "dp_q":
            #get_dp_multi("question", self.db_cnf_dict, qas, 0, len(qas))
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(get_dp_multi, "question", self.db_cnf_dict, qas, n, r) for n in range(0, len(qas), r)}
        elif type == "patch":
            #patch(table_name, qas, 0, r)
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(patch, table_name, qas, n, r) for n in range(0, len(qas), r)}
        elif type == "re_patch":
            # re_patch(table_name, qas, 0, r) # 위 r 의 수를 re_patch 해서 나온 오류 개수 만큼 늘려줘야함.
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(re_patch, table_name, qas, n, r) for n in range(0, len(qas), r)}
        elif type == "check_dp_length":
            #check_dp_length(self.db_cnf_dict, qas, 0, r)
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                fs = {exe.submit(check_dp_length, self.db_cnf_dict, qas, n, r) for n in range(0, len(qas), r)}
        elif type == "context":
            morph_core(table_name, qas, 0, r)
            # with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
                # fs = {exe.submit(morph_core, table_name, qas, n, r) for n in range(0, len(qas), r)}

    def get_dp(self, q):
        c_id = q[0]
        ctx = q[1]
        dp = self.nlp_analyze.get_dependency_parser_result(ctx)
        sql = "UPDATE all_context SET context_dp = %s WHERE id = %s;"
        self.cur.execute(sql, (str(dp), c_id))

    def longtext(self):
        sql = "SELECT id, context FROM all_context WHERE id = %s;"
        self.cur.execute(sql, (2,))
        row = self.cur.fetchone()
        dp_content = self.nlp_analyze.get_dependency_parser_result(row[1])
        update_sql = "UPDATE all_context SET context_dp = %s WHERE id = %s"
        self.cur.execute(update_sql, (str(dp_content), row[0]))
        logger.info("finished")

    def create_dev_kang(self):
        qid_list = list()
        with open("dev_qids.txt") as f:
            for line in f:
                qid_list.append(line.strip())
        qid_part = ', '.join(list(map(lambda x: '%s', qid_list)))
        sql = "INSERT INTO dev_qna_kang SELECT * FROM all_qna " \
              "WHERE q_id IN ({});".format(qid_part)
        self.cur.execute(sql, qid_list)

        cid_list = list()
        for qid in qid_list:
            sql = "SELECT c_id FROM all_qna WHERE q_id = %s;"
            self.cur.execute(sql, (qid,))
            c_id = self.cur.fetchone()[0]
            logger.info(c_id)
            cid_list.append(c_id)
        cid_list = list(set(cid_list))
        cid_part = ', '.join(list(map(lambda x: '%s', cid_list)))
        sql = "INSERT INTO dev_context_kang SELECT * FROM all_context " \
              "WHERE id IN ({});".format(cid_part)
        self.cur.execute(sql, cid_list)

def check_dp_length(self, qas, n, r):
    exec("j{} = SquadDb()".format(n))
    processed_ctx_list = list()
    logger.info("processing: {} ..< {}".format(n, n + r))
    for q in qas[n:n+r]:
        # id, context, context_morph, context_dp
        c_id = q[0]; ctx = q[1]; ctx_morph = q[2]; ctx_dp = q[3]
        new_ctx = eval("j{}".format(n)).nlp_analyze.get_tree_result(ctx)
        try:
            assert(len([x for x in eval(ctx_dp) if x['id'] == 0]) == len(eval(ctx_morph)))
        except AssertionError:
            logger.critical("Different sentence length: {}".format(c_id))
            with open("check/sentence_length.txt", "a") as f:
                f.write("{}\n".format(c_id))
            try:
                assert(len([x for x in eval(ctx_dp) if x['id'] == 0]) == len(new_ctx))
            except AssertionError:
                logger.error("len of new_dp != len of ctx_morph: {}".format(c_id))
                exit()
            '''if "-" in c_id:
                c_id = c_id.split("-")[0]
            if c_id not in processed_ctx_list:
                update_sql = "UPDATE all_context SET context_morph = %s WHERE id = %s;"
                eval("j{}".format(n)).cur.execute(update_sql, (str(new_ctx), c_id))
                logger.info("ctx_morph update")'''

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

def patch(table_name, qas, n, r):
    exec("j{} = SquadDb()".format(n))
    print("j{} = SquadDb()".format(n))
    eval("j{}.connect_db('{}')".format(n, table_name))
    logger.info("Finish connecting to database...: {}".format(n))

    logger.info("processing: {} ..< {}".format(n, n + r))
    processed_ctx = list()
    for q in qas[n:n+r]:
        # q: c_id, q_id, answer, answer_start, context
        c_id = q[0]; q_id = q[1]; answer = q[2]; answer_s = q[3]; ctx = q[4]
        new_s, new_e, new_ctx, new_ans, is_skip, sentence_list = \
            eval("j{}".format(n)).extract_passage(ctx, answer, answer_s, c_id, q_id)
        if is_skip:
            logger.error(q)
            exit()
        logger.info(new_ans)
        if c_id not in processed_ctx:
            if "-" in c_id:
                depend_id = c_id.split("-")[0]; u_id = c_id.split("-")[1]
                sql = "UPDATE all_context_diff SET context_morph = %s WHERE depend_id = %s AND u_id = %s;"
                eval("j{}".format(n)).cur.execute(sql, (str(new_ctx), depend_id, u_id))
            else:
                sql = "UPDATE all_context SET context_morph = %s WHERE id = %s;"
                eval("j{}".format(n)).cur.execute(sql, (str(new_ctx), c_id))
            logger.info("Update c: {}".format(c_id))
        sql = "UPDATE all_qna SET answer_start_morph = %s, answer_end_morph = %s, answer_morph = %s " \
              "WHERE c_id = %s AND q_id = %s;"
        eval("j{}".format(n)).cur.execute(sql, (new_s, new_e, str(new_ans), c_id, q_id))
        logger.info("Update q: {}".format(q_id))

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
    if len(return_list) != 0:
        with open("check/re_patch_{}.txt".format(n), "a") as f:
            f.write("\n".join(return_list))
            f.write("\n")

def get_dp_multi(type, db_cnf, qas, n, r):
    exec("j{} = SquadDb()".format(n))
    print("j{} = SquadDb()".format(n))
    eval("j{}.connect_db()".format(n))
    logger.info("Finish connecting to database...: {}".format(n))

    logger.info("processing: {} ..< {}".format(n, n + r))
    for q in qas[n:n+r]:
        c_id = q[0]
        if type == "context":
            txt = q[1]
        elif type == "question":
            q_id = q[1]
            txt = q[2]
        else:
            logger.error("get_dp_multi - type is wrong. stop process..")
            exit()
        dp = eval("j{}".format(n)).nlp_analyze.get_dependency_parser_result(txt)
        logger.debug(dp)
        if type == "context":
            sql = "UPDATE all_context SET context_dp = %s WHERE id = %s;"
            eval("j{}".format(n)).cur.execute(sql, (str(dp), c_id))
        elif type == "question":
            sql = "UPDATE all_qna SET question_dp = %s WHERE c_id = %s AND q_id = %s;"
            eval("j{}".format(n)).cur.execute(sql, (str(dp), c_id, q_id))

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

def morph_core(table_name, qas, n, r):
    exec("j{} = SquadDb()".format(n))
    eval("j{}.connect_db('{}')".format(n, table_name))
    logger.info("Finish connecting to database...: {}".format(n))
    # c_id, q_id, question, answer, answer_start, context
    logger.info("processing: {} ..< {}".format(n, n + r))
    for q in qas[n:n+r]:
        question = q[2]
        answer = q[3]
        answer_start = q[4]
        context = q[5]
        try:
            assert (context[answer_start:answer_start+len(answer)] == answer)
        except AssertionError:
            logger.info(q[1])
            logger.critical("real answer: {}".format(answer))
            logger.critical("extracted answer: {}".format(context[answer_start:answer_start+len(answer)]))
            exit()

        new_s, new_e, new_ctx, new_answer, isSkip, sentence_list = \
            eval("j{}".format(n)).extract_passage(context, answer, answer_start, q[0], q[1])
        logger.info("isskip: {}".format(isSkip))
        if not isSkip:
            # question
            question_list = eval("j{}".format(n)).nlp_analyze.get_tree_result(question)
            if q[0] not in eval("j{}".format(n)).processed_ctx_list:
                sql = "UPDATE all_context SET context_morph = %s, context_sent = %s WHERE id = %s"
                eval("j{}".format(n)).cur.execute(sql, (str(new_ctx), str(sentence_list), q[0]))
                eval("j{}".format(n)).processed_ctx_list.append(q[0])

            sql = "UPDATE all_qna SET question_morph = %s, answer_morph = %s, " \
                  "answer_start_morph = %s, answer_end_morph = %s " \
                  "WHERE c_id = %s AND q_id = %s;"
            val_tuple = (str(question_list), str(new_answer), new_s, new_e, q[0], q[1])
            logger.debug(val_tuple)
            eval("j{}".format(n)).cur.execute(sql, val_tuple)
            time.sleep(0.2)


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
    elif mode == "context":
        j.process_qa('context', season, db_table)
    elif mode == "q_only":
        j.process_qa('q_only', season, db_table)
    elif mode == "check_data":
        j.check_data(season)
    elif mode == "re_patch":
        j.process_qa('re_patch', season, db_table)
    logger.info("All finished")
