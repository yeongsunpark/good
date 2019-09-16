#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-02

import os, sys
import json
sys.path.append(os.path.abspath('..'))
from pull_module import NewsDbSuper

class NewsDb(NewsDbSuper):
    def __init__(self):
        super(NewsDb, self).__init__()

    def connect_db2(self):
        cfg_dict = self.connect_db()
        self.cur = self.easy_mysql(cfg_dict)

    def select_max(self):
        try:
            sql = "SELECT max(abs(id)) FROM NEWS_SUMMARY.article"
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            return (rows)
        except Exception  as e:
            print (e)

    def insert_data(self, start_id):
        input_dir = "/home/msl/ys/cute/data/news_summary/IT과학"
        for f1 in os.listdir(input_dir):
            with open(os.path.join(input_dir, f1), "r") as f:
                doc = json.load(f)
                title = doc['title']
                article = doc['content']
                summary = doc['summarySentenceList']
                cate = str(input_dir).split("/")[-1]
                file_name = doc['file_name']

            try:
                insert_sql = "INSERT INTO article VALUES (%s, %s, %s, %s, %s, %s)"
                self.cur.execute(insert_sql, (start_id, title, article, str(summary), cate, file_name))
                self.con.commit()
                print (title)
                start_id +=1
            except Exception  as e:
                print (e)
                print(doc)
                break

if __name__ == "__main__":
    j = NewsDb()
    j.connect_db2()
    s_max = j.select_max()
    start_id = s_max[0][0] + 1
    j.insert_data(start_id)
