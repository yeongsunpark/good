#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-20

import os
import sys
import argparse
import logging
import json
sys.path.insert(0,'..')
import ys_logger
from quickstart import main as quick
from comp_with_ori_json import comp_with_ori_json

# log
logger = logging.getLogger('root')
logger.setLevel("INFO") # INFO
logger.addHandler(ys_logger.MyHandler())
logger.info("Logger Setting Finished")

class check():
    # def __init__(self):
        # self.input_dir = "/home/msl/ys/cute/data/sams"

    def main(self, sheet, range_name):
        result = {'version': 'entity_200', 'data': list()}  # 여기에 빼줘야 계속 누적 되어 적힘.
        # f = quick('19_박원아(8/5~)!A1:k3')
        f = quick(sheet+'!'+range_name)
        for ind, line in enumerate(f):
            item = line
            if len(item) == 11:
                q_id = item[0]
                context = item[1]
                question = item[2]
                answer = item[3]
                classify = item[4]
                mod_question = item[5]
                mod_answer = item[6]
                mod_context = item[7]
                remarks = item[8]
                source = item[9]
                source_link = item[10]

            else:
                logger.error("Check len item %s" % len(item))
                break
            conf = comp_with_ori_json(q_id, source, source_link)  # 원본과 비교 후 conf 가져옴.
            # 마커 없는 본문 만들기 (context)
            # 마커 없는 본문에서 정답의 시작 위치 찾기 <- 꼭 확인 해보기. (answer_start)
            # 질문 수정, 정답 수정, 본문 수정 별로 확인하고 True return 하기.

            # answer 부분
            answer_dict = {'text':answer, 'text_fixed':mod_answer, 'answer_start':'Null', 'answer_start_fixed':mod_answer,
                           'source':source, 'source_link':source_link, 'confidence':conf}
            # qas 부분
            question_dict = {'question':question, 'question_fixed':mod_question, 'id':q_id, 'check':classify, 'is_impossible':False,
                             'answers':list()}
            question_dict['answers'].append(answer_dict)
            # context 부분
            context_dict = {'context':"Null", 'context_fixed':mod_context, 'context_with_answer':context, "qas":list()}
            context_dict['qas'].append(question_dict)
            # 최종
            para_dict = {'paragraphs':list()}
            para_dict['paragraphs'].append(context_dict)
            result['data'].append(para_dict)

        with open("/home/msl/ys/cute/data/sams2/final_test.json", "w") as f2:
            json.dump(result, f2, ensure_ascii=False, indent=2)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sheet_name', type=str, default=None)
    parser.add_argument('-r', '--range_name', type=str, default=None)
    args = parser.parse_args()


    if args.sheet_name != None:
        sheet = args.sheet_name
        range_name = args.range_name
    else:
        sheet = "19_박원아(8/5~)"
        range_name = "A2:k3"  # From A2

    c = check()
    c.main(sheet, range_name)