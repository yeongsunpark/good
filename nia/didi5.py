#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by YeongsunPark at 2019-02-27
import sys, os
import json
import time
result = dict()
result['version'] = 1
result['creator'] = "MINDs Lab."
result['data'] = list()
passage_list = list()
number = 1
l = []
i = 1
with open("/home/msl/ys/cute/nia/common_tsv/크웍18전달건_편집_질문번호_ascending_num바꿈.txt", "r") as f:
    # title content 질문번호 질문 유사질문 답변 기사일자 원본 답시작 답끝
    # for line in f:
    a = 1
    while True:
        line = f.readline()
        item = line.strip().split("\t")
        if len(item) == 10:
            para_dict = dict()
            para_dict['main_qa_list'] = list()
            title = item[0]
            context_ori = item[7]
            number += 1
            q_id = item[2]
            q_1 = item[3]
            answer = item[4]
            wh = ""
            answer_s = item[8]
            answer_e = item[9]


            if context_ori[int(answer_s):int(answer_e)] != answer:
                # print (answer, context_ori[int(answer_s):int(answer_e)])
                continue
            else:
                qas_dict = dict()
                # qas_dict['number'] = number
                qas_dict['q_id'] = q_id
                qas_dict['question'] = q_1
                qas_dict['answer'] = answer
                qas_dict['begin'] = answer_s
                qas_dict['end'] = answer_e

                qas_dict['classType'] = ""
                qas_dict['type'] = ""
                qas_dict['isFlexible'] = 0
                para_dict['main_qa_list'].append(qas_dict)
                ####
                para_dict['seq'] = i
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


        if a == 3000:
            break
        a += 1

            #except:
            #    print(context_ori)
f = open("/home/msl/ys/cute/nia/common_tsv/didi4_0423.json", "w")
json.dump(result, f, ensure_ascii=False, indent=2)
