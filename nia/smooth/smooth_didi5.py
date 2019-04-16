#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by YeongsunPark at 2019-02-27
import sys, os
import json
import time
import check_wh

# 답 없는 엑셀을 위해 만듦
result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()
passage_list = list()
wh_dict = {"work_who":0, "work_when":1, "work_where":2, "work_what":3, "work_how":4, "work_why":5, "":""}

l = []
i = 1  # 수정
q_id = 1
# with open(sys.argv[1], "r") as f:
with open("/home/msl/ys/cute/nia/asdf.tsv", "r") as f:
    # TITLE context 질문유형 질문
    ti = ""
    con = ""
    for line in f:
        item = line.strip().split("\t")
        # print (len(item))
        if len(item) == 4:
            title = item[0].strip()
            ti = title
            context_ori = item[1].strip()
            con = context_ori
            wh = item[2].strip()
            q_1 = item[3].strip()
        elif len(item) == 2:
            title = ti
            context_ori = con
            wh = item[0].strip()
            q_1 = item[1].strip()
        else:
            print (line)
            continue

        if wh == "":
            break

        para_dict = dict()
        para_dict['main_qa_list'] = list()

        qas_dict = dict()
        qas_dict['q_id'] = q_id  # 크웍엔 없음
        qas_dict['question'] = q_1
        qas_dict['answer'] = ""
        qas_dict['begin'] = ""
        qas_dict['end'] = ""
        qas_dict['classType'] = check_wh.change_wh(wh)
        qas_dict['type'] = wh_dict[qas_dict['classType']]
        qas_dict['isFlexible'] = 0
        para_dict['main_qa_list'].append(qas_dict)

        para_dict['seq'] = title
        para_dict['text'] = context_ori
        para_dict['source'] = 0
        para_dict['doc_type'] = 0
        para_dict['sub_doc_type'] = 0
        para_dict['fileName'] = i
        if context_ori not in l:
            result['data'].append(para_dict)
            l.append(context_ori)
            i += 1
        else:
            for p in result['data']:
                if p['text'] == context_ori:
                    p['main_qa_list'].append(qas_dict)
        q_id +=1

f = open("/home/msl/ys/cute/nia/smooth/new_normal_finish_sum5.json", "w")
# f = open(sys.argv[2], "w")
json.dump(result, f, ensure_ascii=False, indent=2)
f.close()