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
        self.input_dir = "/home/msl/ys/cute/data/re_law/파일럿과1차"

    def connect_db2(self):
        cfg_dict = self.connect_db()  # cfg_dict = pull_module.SquadDb.connect_db(self)
        self.cur = self.easy_mysql(cfg_dict)  # self.cur = pull_module.SquadDb.easy_mysql(self, cfg_dict)


    def insert_context(self):
        print('insert start')
        max_c_id = 1
        for fl in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, fl), "r") as f:
                json_data1 = json.load(f)
                name = fl.split("_")[1]
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
                try:
                    insert_memo_sql = 'INSERT INTO all_context values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    category_id = max_c_id

                    self.cur.execute(insert_memo_sql, (category_id, document_id, statute_code, law_name, public_date,
                                                       belong_no, belong_title, article_no, article_title, article_content,
                                                       law_in_q, file_name))
                    self.con.commit()
                    max_c_id += 1
                except:
                    print("try again")

    def insert_question(self, max_q_id):
        print('insert start')
        for fl in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, fl), "r") as f:
                print (fl)
                json_data1 = json.load(f)
                name = fl.split("_")[1]
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
                        insert_memo_sql = 'INSERT INTO all_qna values(%s, %s, %s, %s, %s, %s, %s)'
                        q_id = max_q_id
                        self.cur.execute(insert_memo_sql,
                                         (c_id, q_id, question, answer_start, answer_end, text, level))
                        self.con.commit()
                        max_q_id += 1
                    except:
                        print("try again")

    def select_c_id(self, document_id):
        select_sql = 'select id from all_context where document_id = %s'
        self.cur.execute(select_sql, document_id)
        selected_c_id = self.cur.fetchall()
        self.con.commit()
        if len(selected_c_id) == 1:
            return selected_c_id[0][0]

    def max_q(self):
        select_max_q = 'select max(abs(q_id)) from all_qna'
        self.cur.execute(select_max_q)
        selected_max_q = self.cur.fetchall()
        self.con.commit()
        print (len(selected_max_q))
        if len(selected_max_q) == 1:
            return 0
        else:
            return int(selected_max_q[0][0])

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    m_q_id = j.max_q()
    j.insert_question(m_q_id+1)
