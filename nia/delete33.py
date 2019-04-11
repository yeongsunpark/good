#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-11

import pymysql

def return_myself(token):
    return token

class SquadDb():

    def __init__(self):

        self.con = None
        self.cur = None

    def easy_mysql(self, cfg_dict, encoding='utf8', autocommit=False):
        self.con = pymysql.connect(host=cfg_dict['host'], user=cfg_dict['usr'],
                                   passwd=cfg_dict['pwd'], db=cfg_dict['db'], charset=encoding)
        self.cur = self.con.cursor()
        if autocommit is True:
            self.con.autocommit(True)

    def connect_db(self, table_name):
        try:        # try to connect to project db
            cfg_dict = dict(host='localhost', usr= 'root', pwd='data~secret!', db=table_name)
            self.easy_mysql(cfg_dict, encoding='utf8', autocommit=True)
            self.cur.execute("SET NAMES utf8")
        except Exception as e:
            print ("Finish connecting to database...")

    def work(self):
        sql = "SELECT * FROM all_context GROUP BY seq HAVING COUNT(seq) > 1"
        self.cur.execute(sql)
        row = self.cur.fetchall()

if __name__ == "__main__":

    db_table = "SQUAD_NEWS_NIA"

    j = SquadDb()
    j.connect_db(db_table)
    j.work()