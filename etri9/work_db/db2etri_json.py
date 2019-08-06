#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-31

import os, sys
import logging
import json
from pull_module import SquadDbSuper
import ys_logger
sys.path.append(os.path.abspath('..'))

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(ys_logger.MyHandler())
logger.info("Finish setting logger")


class SquadDb(SquadDbSuper):
    def __init__(self):
        super(SquadDb, self).__init__()  # pull_module.SquadDbSuper 의 __init__ (self) 아래 속성 가져옴.
        self.start_id = 19000000
        self.output_dir = "/home/msl/ys/cute/data/re_law"

    def connect_db2(self):
        cfg_dict = self.connect_db()  # cfg_dict = pull_module.SquadDb.connect_db(self)
        self.cur = self.easy_mysql(cfg_dict)  # self.cur = pull_module.SquadDb.easy_mysql(self, cfg_dict)

    def db2squad(self):
        # context 부분
        fetch_sql_ctx = "SELECT document_id, statute_code, law_name, public_date, belong_no, belong_title, " \
                        "article_no, article_title, article_content, law_in_q FROM all_context order by abs(document_id);"
        self.cur.execute(fetch_sql_ctx)
        contexts = self.cur.fetchall()   # entire

        result = dict()
        result['version'] = "MINDsLab_2019"
        result['creator'] = "MINDsLab"
        result['data'] = list()

        # question 부분
        for context in contexts:
            pre_result = dict()
            pre_result['paragraphs'] = list()
            qas_list = list()
            fetch_sql_qa = "SELECT question, answer_start, answer_end, answer, level FROM all_qna " \
                            "WHERE d_id='{}'".format(context[0])
            self.cur.execute(fetch_sql_qa)

            public_date = context[3]
            article_content = context[8]
            statute_code = context[1]
            document_id = context[0]
            article_no = context[6]
            article_title = context[7]
            belong_title = context[5]
            belong_no = context[4]
            law_name = context[2]
            law_written_in_q = context[9]  # 0724추가

            for row in self.cur.fetchall():
                self.start_id +=1
                q_id = self.start_id
                """
                qas_dict = {'id': q_id, 'question':row[0], 'question_level':row[4], 'question_en': '',
                            'question_tagged':'', 'questionType':'', 'questionFocus':'',
                            'questionSAT':'', 'questionLAT':'', 'lawName':'', 'answers':list()}
                """
                qas_dict = {'id': q_id, 'question':row[0], 'question_level':row[4], 'question_en': '',
                            'question_tagged':'', 'questionType':'', 'questionFocus':'',
                            'questionSAT':'', 'questionLAT':'', 'lawName':law_written_in_q, 'answers':list()}
                qas_list.append(qas_dict)

                qas_dict['answers'].append(
                    {'text': row[3], 'answer_start': row[1], 'answer_end': row[2],
                     'text_en': '', 'text_tagged': '', 'text_syn': ''})


            data_dict = {'qas': qas_list, 'context_id':document_id, 'context': article_content, 'context_en': '', 'context_tagged':''}

            pre_result['paragraphs'].append(data_dict)
            pre_result['title'] = law_name

            result['data'].append(pre_result)

        f2 = open(os.path.join(self.output_dir, "law_20190806.json"), "w", encoding='utf-8')
        json.dump(result, f2, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    j.db2squad()
