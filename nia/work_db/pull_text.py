# -*- coding: utf-8 -*-

import logging
import os, sys

import pymysql

sys.path.append(os.path.abspath('..'))
# import custom_logger
import csv



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
        f = open("/home/msl/ys/cute/nia/season6_text.txt" ,"w")
    
        try:
            # select_sql = 'select c_id, q_id, question, answer from SQUAD_KO_ORI.all_qna WHERE q_id =%s'
            # select_sql2 = 'select char_length(context) from all_context'
            select_sql3 = 'select id, context from all_context where season = 6'
            # self.cur.execute(select_sql, (q_id))
            # self.cur.execute(select_sql2)
            self.cur.execute(select_sql3)
            select_data_row = self.cur.fetchall()
            print (len(select_data_row))
            self.con.commit()
            for i in range(len(select_data_row)):
                #f.write(str(select_data_row[i][0]))
                #f.write("\n")

                f.write(select_data_row[i][0])
                f.write("\t")
                f.write(select_data_row[i][1])
                f.write("\n")
        except:
            print("no")
        
        """
        try:
            fetch_sql_ctx = "SELECT id, title, context FROM all_context_all"
            self.cur.execute(fetch_sql_ctx)
            contexts = self.cur.fetchall()  # entire

            for context in contexts:
                fetch_sql_qa = "SELECT q_id, answer_start, answer_end, answer FROM all_qna " \
                                "WHERE c_id='{}'".format(context[0])
                self.cur.execute(fetch_sql_qa)
                for row in self.cur.fetchall():
                    id = row[0]
                    a_s = row[1]
                    a_e = row[2]
                    answer = row[3]

                    if context[2][a_s:a_e] != answer:
                        # print (row)
                        f.write(str(row))
                        f.write("\n")
        except:
            print ("no")
        """
if __name__ == "__main__":
    j = SquadDb()
    j.connect_db()
    j.select_data()
    # j.update_data()
    # j.count_data()
    # j.insert_data()
    # logger.info("All finished")
