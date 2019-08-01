#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-31

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

    def select_data5(self):
        f = open("/home/msl/ys/cute/data/re_law/important.txt" ,"w")
        imp_law_name = ["국가안전보장회의법", "국회도서관법", "국회의원수당 등에 관한 법률", "국회사무처법", "국회에서의 증언ㆍ감정 등에 관한 법률",
                        "대한민국헌정회 육성법", "국정감사 및 조사에 관한 법률", "대한민국헌법"]
        result = []
        try:
            fetch_sql_qas = "select c.document_id, c.law_name, c.article_content, c.law_in_q, q.q_id, q.question, q.answer, q.level " \
                            "from all_context as c " \
                            "left join all_qna as q " \
                            "on c.document_id = q.d_id " \
                            "where law_name = %s"
            for l in imp_law_name:
                self.cur.execute(fetch_sql_qas, l)
                data = self.cur.fetchall()
                for d in data:
                    f.write("\t".join(d))
                    f.write("\n")

        except:
            print ("no select_data")

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    j.select_data5()