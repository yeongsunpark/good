#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by YeongsunPark at 2019-02-27
import sys, os
import json
import time
import check_wh


result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()
passage_list = list()
wh_dict = {"work_who":0, "work_when":1, "work_where":2, "work_what":3, "work_how":4, "work_why":5}

l = []
i = 1  # 수정
# with open(sys.argv[1], "r") as f:
with open("/home/msl/ys/cute/nia/smooth/new_normal_finish-sum3.txt", "r") as f:
    # TITLE context 질문번호    질문    답변    카테고리    육하원칙    원본    답 시작위치 답 끝위치
    for line in f:
        item = line.strip().split("\t")
        # print (len(item))
        if len(item) == 10:
            para_dict = dict()
            para_dict['main_qa_list'] = list()

            title = item[0]
            context_ori = item[7].strip()
            q_id = item[2].strip()
            q_1 = item[3]
            answer = item[4]
            wh = item[6].strip()
            if wh == "":
                break
            answer_s = item[8]
            answer_e = item[9]

            qas_dict = dict()
            qas_dict['q_id'] = q_id  # 크웍엔 없음
            qas_dict['question'] = q_1
            qas_dict['answer'] = answer
            qas_dict['begin'] = answer_s
            qas_dict['end'] = answer_e
            # qas_dict['classType'] = wh_dict[wh.strip()]
            if wh == ' ':
                print (line)
            else:
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
                i+=1
            else:
                for p in result['data']:
                    if p['text'] == context_ori:
                        p['main_qa_list'].append(qas_dict)
        else:
            print (line)
            break
            #except:
            #    print(context_ori)

f = open("/home/msl/ys/cute/nia/smooth/new_normal_finish_sum3.json", "w")
# f = open(sys.argv[2], "w")
json.dump(result, f, ensure_ascii=False, indent=2)
f.close()
