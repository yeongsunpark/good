# -*- coding: utf-8 -*-

import os, sys
import pymysql
from pull_module import SquadDbSuper
sys.path.append(os.path.abspath('..'))
# 본문[시작위치:끝위치] != 답변 찾기용

class SquadDb(SquadDbSuper):
    def __init__(self):
        super(SquadDb, self).__init__()
        # self.db_cnf_dict = {"host": '10.122.64.83', "usr": "root", "pwd": "data~secret!",
        #                     "db": "SQUAD_NEWS_NIA", "encoding": "utf8"}
        # self.con = None
        # self.cur = None

    def connect_db2(self):
        # pull_module.SquadDb.connect_db(self)
        # self.connect_db()
        # cfg_dict = pull_module.SquadDb.connect_db(self)
        # print (cfg_dict)
        # self.cur = pull_module.SquadDb.easy_mysql(self, cfg_dict)

        cfg_dict = self.connect_db()
        print(cfg_dict)
        self.cur = self.easy_mysql(cfg_dict)

    def select_data(self):
        f = open("/home/msl/ys/cute/nia/sw.txt" ,"w")
        result = []
        try:
            a =0
            fetch_sql_ctx = "SELECT id, context FROM all_context "
            try:
                self.cur.execute(fetch_sql_ctx)
            except:
                print ("nnnnnnno")
            contexts = self.cur.fetchall()  # entire
            print (len(contexts))

            for context in contexts:

                fetch_sql_qa = "SELECT q_id, answer_start, answer_end, answer FROM all_qna " \
                                "WHERE c_id='{}'".format(context[0])
                self.cur.execute(fetch_sql_qa)
                for row in self.cur.fetchall():
                    id = row[0]
                    a_s = int(row[1])
                    a_e = int(row[2])
                    answer = row[3]

                    if context[1][a_s:a_e] != answer:
                        result.append("\t".join([str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(context[0]), str(context[1])]))
            for d in result:
                f.write(d)
                f.write("\n")

        except:
            print ("no")

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    j.select_data()