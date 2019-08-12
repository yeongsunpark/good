# -*- coding: utf-8 -*-

import os, sys
from pull_module import SquadDbSuper
sys.path.append(os.path.abspath('..'))
# 본문[시작위치:끝위치] != 답변 찾기용

class SquadDb(SquadDbSuper):
    def __init__(self):
        super(SquadDb, self).__init__()  # pull_module.SquadDbSuper 의 __init__ (self) 아래 속성 가져옴.
        self.input_dir = "/home/msl/ys/cute/data/re_law/파일럿과1차"

    def connect_db2(self):
        cfg_dict = self.connect_db()  # cfg_dict = pull_module.SquadDb.connect_db(self)
        self.cur = self.easy_mysql(cfg_dict)  # self.cur = pull_module.SquadDb.easy_mysql(self, cfg_dict)

    def select_data(self):

        f = open("/home/msl/ys/cute/nia/sw_new.txt" ,"w")
        result = []
        try:
            a =0
            fetch_sql_ctx = "SELECT id, context FROM all_context "
            try:
                self.cur.execute(fetch_sql_ctx)
            except:
                print ("no connect_db2")
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
            print ("no select_data")

    def select_data2(self):
        f = open("/home/msl/ys/cute/nia/sw_dup2.txt" ,"w")
        result = []
        try:
            fetch_sql_qa = "SELECT q.q_id, q.question, q.answer, c.context, count(*) as num " \
                           "FROM all_qna as q inner join all_context as c on q.c_id = c.id " \
                           "GROUP BY q.question, q.answer, c.context " \
                           "HAVING num>1 order by num "
            self.cur.execute(fetch_sql_qa)
            for row in self.cur.fetchall():
                result.append("\t".join([str(row[0]), str(row[1]), str(row[2]), str(row[3])]))
            for d in result:
                f.write(d)
                f.write("\n")

        except:
            print ("no select_data")

    def select_data3(self):
        f = open("/home/msl/ys/cute/nia/sw_req.txt" ,"w")
        result = []
        try:
            fetch_sql_qa = "SELECT question, answer, reason " \
                           "FROM all_qna " \
                           "where q_id like 'm4%-1'"
            self.cur.execute(fetch_sql_qa)
            for row in self.cur.fetchall():
                result.append("\t".join([str(row[0]), str(row[1]), str(row[2])]))
            for d in result:
                f.write(d)
                f.write("\n")

        except:
            print ("no select_data")

    def select_data4(self):
        f = open("/home/msl/ys/cute/nia/no_wh27.txt" ,"w")
        result = []
        try:
            fetch_sql_qa = "SELECT c_id, q_id, question " \
                           "FROM all_qna_error " \
                           "where (classType is null or classType = '') and q_id like '%-1'"
            self.cur.execute(fetch_sql_qa)
            for row in self.cur.fetchall():
                result.append("\t".join([str(row[0]), str(row[1]), str(row[2])]))
            for d in result:
                f.write(d)
                f.write("\n")

        except:
            print ("no select_data")

    def select_data5(self):
        f = open("/home/msl/ys/cute/nia/text/eco_29.txt" ,"w")
        result = []
        try:
            fetch_sql_qa = "SELECT id, context " \
                           "FROM all_context_error " \
                           "where source = 2 and context not like '%거래%' and context not like '%코스닥%' "
            self.cur.execute(fetch_sql_qa)
            for row in self.cur.fetchall():
                result.append("\t".join([str(row[0]), str(row[1])]))
            for d in result:
                f.write(d)
                f.write("\n")

        except:
            print ("no select_data")

if __name__ == "__main__":
    j = SquadDb()
    j.connect_db2()
    j.select_data5()