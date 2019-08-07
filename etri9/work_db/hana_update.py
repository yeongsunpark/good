#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-07

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

    def update_data(self):
        header = True
        f = open("/home/msl/ys/cute/data/title_replace.txt", "r")
        try:
            for data in f:
                if header:
                    header = False
                    continue
                item = data.replace("\n","").split("\t")
                old_title = item[0]
                new_title = item[1]
                update_sql = "update hana_all_context set title = %s where title = %s"
                self.cur.execute(update_sql, (new_title, old_title))
                self.con.commit()

        except:
            print("no select_data")


if __name__ == "__main__":
     j = SquadDb()
     j.connect_db2()
     j.update_data()