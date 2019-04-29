# -*- coding: utf-8 -*-

import os, sys
import pymysql

sys.path.append(os.path.abspath('..'))
# 본문[시작위치:끝위치] != 답변 찾기용
class SquadDb():

    def __init__(self):
        self.db_cnf_dict = {"host": '10.122.64.83', "usr": "root", "pwd": "data~secret!",
                            "db": "SQUAD_NEWS_NIA", "encoding": "utf8"}
        self.con = None
        self.cur = None
        self.connect_db()

    def easy_mysql(self, cfg_dict, encoding='utf8', autocommit=False):
        self.con = pymysql.connect(host=cfg_dict['host'], user=cfg_dict['usr'],
                                   passwd=cfg_dict['pwd'], db=cfg_dict['db'], charset=encoding)
        self.cur = self.con.cursor()
        if autocommit is True:
            self.con.autocommit(True)

    def connect_db(self):
        try:        # try to connect to project db
            cfg_dict = dict(host=self.db_cnf_dict['host'], usr=self.db_cnf_dict['usr'],
                            pwd=self.db_cnf_dict['pwd'], db=self.db_cnf_dict['db'])
            self.easy_mysql(cfg_dict, encoding=self.db_cnf_dict['encoding'], autocommit=True)     # turn-on autocummit, be careful!
            self.cur.execute("SET NAMES utf8")
            print ("hi")
        except Exception as e:
            pass
    def select_data(self):
        f = open("/home/msl/ys/cute/nia/sw.txt" ,"w")
        result = []
        try:
            a =0
            fetch_sql_ctx = "SELECT id, context FROM all_context "
            self.cur.execute(fetch_sql_ctx)
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
    j.connect_db()
    j.select_data()
