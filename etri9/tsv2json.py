#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-10

import json

f = open("/home/msl/ys/cute/data/cw_law/result_0607/3672.txt")
dic = dict()
data_dic = dict()
p_dic = dict()
q_dic = dict()
a_dic = dict()

data_dic["paragraphs"] = list()
p_dic["qas"] = list()
q_dic["answers"] = list()
for ff in f:
    ff = ff.strip("\n")
    item = ff.split("\t")
    dic["data"] = list()
    if len(item) == 6:
        if item[0] == "version":
            dic["version"] = item[-1]
        if item[0] == "creator":
            dic["creator"] = item[-1]

        if item[1] == "title":
            data_dic["title"] = item[-1]

        if item[2] == "context_id":
            p_dic["context_id"] = item[-1]
        if item[2] == "공포일자":
            p_dic["공포일자"] = item[-1]
        if item[2] == "법령코드":
            p_dic["법령코드"] = item[-1]
        if item[2] == "조번호":
            p_dic["조번호"] = item[-1]
        if item[2] == "조제목":
            p_dic["조제목"] = item[-1]
        if item[2] == "소속제목":
            p_dic["소속제목"] = item[-1]
        if item[2] == "소속번호":
            p_dic["소속번호"] = item[-1]
        if item[2] == "context":
            p_dic["context"] = item[-1]
        if item[2] == "context_en":
            p_dic["context_en"] = item[-1]
        if item[2] == "context_tagged":
            p_dic["context_tagged"] = item[-1]

        if item[3] == "id":
            q_dic["id"] = item[-1]
        if item[3] == "question":
            q_dic["question"] = item[-1]
        if item[3] == "난이도":
            q_dic["난이도"] = item[-1]
        if item[3] == "question_en":
            q_dic["question_en"] = item[-1]
        if item[3] == "question_tagged":
            q_dic["question_tagged"] = item[-1]
        if item[3] == "questionType":
            q_dic["questionType"] = item[-1]
        if item[3] == "questionFocus":
            q_dic["questionFocus"] = item[-1]
        if item[3] == "questionSAT":
            q_dic["questionSAT"] = item[-1]
        if item[3] == "questionLAT":
            q_dic["questionLAT"] = item[-1]

        if item[4] == "text":
            a_dic["text"] = item[-1]
        if item[4] == "text_en":
            a_dic["text_en"] = item[-1]
        if item[4] == "text_tagged":
            a_dic["text_tagged"] = item[-1]
        if item[4] == "text_syn":
            a_dic["text_syn"] = item[-1]
        if item[4] == "answer_start":
            a_dic["answer_start"] = item[-1]
        if item[4] == "answer_end":
            a_dic["answer_end"] = item[-1]


q_dic["answers"].append(a_dic)
p_dic["qas"].append(q_dic)
data_dic["paragraphs"].append(p_dic)
dic["data"].append(data_dic)

"""
data_dic["question"] = list()
q_dic = dict()
q_dic["question_id"] = "1"
q_dic["question_context"] = "q1"
q_dic["paragraphs"] = list()

p_dic = dict()
p_dic["id"] = "p1"
p_dic["title"] = "ti"
p_dic["context"] = "cc"
p_dic["answer"] = list()

a_dic = dict()
a_dic["answer_text"] = "t"
a_dic["answer_start"] = 1
a_dic["answer_end"] = 2

p_dic["answer"].append(a_dic)
q_dic["paragraphs"].append(p_dic)
data_dic["question"].append(q_dic)

dic["data"].append(data_dic)

print (dic)
"""
jsonString = json.dumps(dic, ensure_ascii=False)
print (jsonString)
f.close()