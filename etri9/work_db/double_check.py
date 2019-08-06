#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-06

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
        f = open("/home/msl/ys/cute/data/re_law/no_law_name2.txt", "w")
        try:
            fetch_sql_qas = "select c.document_id, c.law_name, c.law_in_q, q.question " \
                            "from all_context as c " \
                            "left join all_qna as q " \
                            "on c.document_id = q.d_id "
            self.cur.execute(fetch_sql_qas)
            data = self.cur.fetchall()
            for d in data:
                if (d[1] in d[3]) and d[2] == "":
                    f.write("\t".join(d))
                    f.write("\n")
                    # update_sql = "update all_context set law_in_q = %s where document_id = %s"
                    # self.cur.execute(update_sql, (d[1], d[0]))
                    # self.con.commit()

        except:
            print("no select_data")


if __name__ == "__main__":
     j = SquadDb()
     j.connect_db2()
     j.select_data5()
