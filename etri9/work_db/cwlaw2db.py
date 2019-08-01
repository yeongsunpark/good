#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-25

import os, sys
import json
from pull_module import SquadDbSuper
sys.path.append(os.path.abspath('..'))

class SquadDb(SquadDbSuper):
    def __init__(self):
        super(SquadDb, self).__init__()  # pull_module.SquadDbSuper 의 __init__ (self) 아래 속성 가져옴.

    def connect_db2(self):
        cfg_dict = self.connect_db()  # cfg_dict = pull_module.SquadDb.connect_db(self)
        self.cur = self.easy_mysql(cfg_dict)  # self.cur = pull_module.SquadDb.easy_mysql(self, cfg_dict)


    def insert_context(self, max_c_id, season, input_dir):
        print('insert start')
        for fl in os.listdir(input_dir):
            with open(os.path.join(input_dir, fl), "r") as f:
                print (fl)
                json_data1 = json.load(f)
                if fl.count("_") == 2:
                    name = fl.split("_")[1]
                else:
                    name = fl.split("_")[0]
                json_data = json_data1[name]

                document_id = json_data["문서ID"]
                statute_code = json_data["법령코드"]
                law_name = json_data["법령명"]
                public_date = json_data["공포일자"]
                belong_no = json_data["소속번호"]
                belong_title = json_data["소속제목"]
                article_no = json_data["조번호"]
                article_title = json_data["조제목"]
                article_content = json_data["조내용"]
                law_in_q = json_data["메모"]
                file_name = json_data["파일명"].split("_")[0]
                ref_context = json_data["질문참고본문"]
                try:
                    insert_memo_sql = 'INSERT INTO all_context values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    category_id = max_c_id

                    self.cur.execute(insert_memo_sql, (category_id, document_id, statute_code, law_name, public_date,
                                                       belong_no, belong_title, article_no, article_title, article_content,
                                                       law_in_q, ref_context, file_name, season))
                    self.con.commit()
                    max_c_id += 1
                except:
                    print("try again")

    def insert_question(self, max_q_id, input_dir):
        print('insert start')
        for fl in os.listdir(input_dir):
            with open(os.path.join(input_dir, fl), "r") as f:
                print (fl)
                json_data1 = json.load(f)
                if fl.count("_") == 2:
                    name = fl.split("_")[1]
                else:
                    name = fl.split("_")[0]
                json_data = json_data1[name]
                document_id = json_data["문서ID"]
                for i in range(len(json_data["qas"])):
                    qas = json_data["qas"][i]
                    id = qas["id"]
                    question = qas["question"]
                    level = qas["level"]
                    answers = qas["answer"][0]
                    answer_start = answers["answer_start"]
                    answer_end = answers["answer_end"]
                    text = answers["text"]

                    c_id = j.select_c_id(document_id)
                    try:
                        insert_memo_sql = 'INSERT INTO all_qna values(%s, %s, %s, %s, %s, %s, %s, %s)'
                        q_id = max_q_id
                        self.cur.execute(insert_memo_sql,
                                         (c_id, document_id, q_id, question, answer_start, answer_end, text, level))
                        self.con.commit()
                        max_q_id += 1
                    except:
                        print("try again")
                        print (c_id, q_id, document_id, question, answer_start, answer_end, text, level)


    def select_c_id(self, document_id):
        select_sql = 'select id from all_context where document_id = %s'
        self.cur.execute(select_sql, document_id)
        selected_c_id = self.cur.fetchall()
        self.con.commit()
        if len(selected_c_id) == 1:
            return selected_c_id[0][0]

    def max_id(self, type):
        if type == "question":
            select_max = 'select max(abs(q_id)) from all_qna'
        elif type == "context":
            select_max = 'select max(abs(id)) from all_context'
        self.cur.execute(select_max)
        selected_max = self.cur.fetchall()
        self.con.commit()
        print (len(selected_max))
        if selected_max[0][0] is None:
            return 0
        else:
            return int(selected_max[0][0])

if __name__ == "__main__":
    # context 후 question 하기!
    mode = "question"  # context/ question
    season = 2
    if season == 0:
        input_dir = "/home/msl/ys/cute/data/re_law/파일럿과1차_190731/답과3가지질문만들기-파일럿(374건)/답과3가지질문만들기-파일럿(374건)"
    elif season == 1:
        input_dir = "/home/msl/ys/cute/data/re_law/파일럿과1차_190731/답과3가지질문만들기-1차(1474건)/답과3가지질문만들기-1차(1474건)"
    elif season == 2:
        input_dir = "/home/msl/ys/cute/data/re_law/2219-답과3가지질문만들기-2차"
    else:
        print ("no season")

    j = SquadDb()
    j.connect_db2()

    print (j.max_id("question"))

    if mode == "context":
        m_c_id = j.max_id(mode) + 1
        j.insert_context(m_c_id, season, input_dir)
    if mode == "question":
        m_q_id = j.max_id(mode) + 1
        print(m_q_id)
        j.insert_question(m_q_id, input_dir)
