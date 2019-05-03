# -*- coding: utf-8 -*-

import logging
import os, sys

import pymysql

sys.path.append(os.path.abspath('..'))


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
        f = open("/home/msl/ys/cute/nia/190423similar.txt" ,"w")
        try:
            # select_sql = 'select c_id, q_id, question, answer from SQUAD_KO_ORI.all_qna WHERE q_id =%s'
            select_sql2 = 'select category_id, qa_id, question, answer, reason_morpheme from DATA_QA_TB where abs(category_id) >= 120207'
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
    def count_data(self):
        f = open("/home/msl/ys/cute/nia/sw_req.txt" ,"r")
        f2 = open("/home/msl/ys/cute/nia/sw_req_no.txt" ,"w")
        f3 = open("/home/msl/ys/cute/nia/sw_req_yes.txt", "w")
        count = 0
        try:
            for data in f:
                data=data.replace("\n","").replace('"',"'")
                item = data.split("\t")
                select_sql2 = 'select count(*) from DATA_QA_TB where question = "{}" and answer = "{}" and reason_morpheme = "{}"'.format(item[0], item[1], item[2])
                # self.cur.execute(select_sql, (q_id))
                self.cur.execute(select_sql2)
                select_data_row = self.cur.fetchall()
                self.con.commit()
                if select_data_row[0][0] == 1:
                    count +=1
                else:
                    f2.write("\t".join([item[0], item[1], item[2]]))
                    f2.write("\n")
            print (count)
        except:
            print(data)
            print (count)
        f.close()
        f2.close()
        f3.close()



if __name__ == "__main__":
    j = SquadDb()
    j.connect_db()
    j.count_data()