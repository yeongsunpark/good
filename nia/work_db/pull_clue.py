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
                            "db": "MRC_TRAIN", "encoding": "utf8"}
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
        f = open("/home/msl/ys/cute/nia/sw2.txt" ,"w")
        try:
            # select_sql = 'select c_id, q_id, question, answer from SQUAD_KO_ORI.all_qna WHERE q_id =%s'
            select_sql2 = 'select category_id, qa_id, question, answer, reason_morpheme from DATA_QA_TB'
            # self.cur.execute(select_sql, (q_id))
            self.cur.execute(select_sql2)
            select_data_row = self.cur.fetchall()
            print (len(select_data_row))
            self.con.commit()

            for i in range(len(select_data_row)):
                # print(select_data_row[i])
                for k in range(0, 5):
                    f.write(str(select_data_row[i][k]))
                    f.write("\t")
                f.write("\n")

        except:
            print("no")




if __name__ == "__main__":
    j = SquadDb()
    j.connect_db()
    j.select_data()
    # j.update_data()
    # j.count_data()
    # j.insert_data()
    # logger.info("All finished")
