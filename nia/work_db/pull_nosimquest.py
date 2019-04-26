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
        f = open("/home/msl/ys/cute/nia/check/no_simquestion.txt" ,"w")
        try:
            fetch_sql_qa = "select c_id, q_id, question, answer, reason from all_qna where q_id in (select q_id from all_qna where q_id like 'm4%' group by substring_index(q_id, '-', 1) having count(*) = 1);"

            # 22929".format(context[0])
            self.cur.execute(fetch_sql_qa)
            for row in self.cur.fetchall():
                # print (row)
                f.write(str(row[0])+ "\t"+ str(row[1])+ "\t"+ str(row[2])+ "\t"+ str(row[3])+ "\t"+ str(row[4]))
                f.write("\n")
        except:
            print ("no")
        f.close()

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db()
    j.select_data()
