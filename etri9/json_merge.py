#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-17

import sys, os
import json
import re
import logging
import ys_logger as ys_logger

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(ys_logger.MyHandler())
logger.info("Finish setting logger")
fileHandler = logging.FileHandler('./json_merge.log')
logger.addHandler(fileHandler)
fmt = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >>> %(message)s')
fileHandler.setFormatter(fmt)


sys.path.insert(0,'..')

# 과거 json_merge.py 파일과 json2json.py 파일을 합친 것.(# Created by YeongsunPark at 2019-06-18)
class json_merge_and_count():
    def __init__(self):
        self.input_dir = "/home/msl/ys/cute/data/re_law/파일럿과1차"
        self.output_dir = "/home/msl/ys/cute/data/re_law"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.full = True
        self.start_id = 19000000
        self.a = 0
        self.version = "MINDsLab_2019"

    # 낱개를 하나로
    def merge(self):
        # 하기 전에 txt 파일이 utf-8로 인코딩이 되어 있나 꼭 확인하기!
        # utf-8 파일은 제일 윗 줄을 제대로 인식을 못하니 한 줄 띄기!
        result = dict()
        result['version'] = 1
        result['creator'] = "MINDs Lab."
        result['data'] = list()
        for file in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, file), "r") as f:
                json_data1 = json.load(f)
                result['data'].append(json_data1)
        with open(os.path.join(self.output_dir, "파일럿과1차sum.json"), "w") as f2:
            json.dump(result, f2, indent=2, ensure_ascii=False)

    def refine(self):
        with open(os.path.join(self.output_dir, "파일럿과1차sum.json"), "r", encoding='utf-8') as f1:
            doc = json.load(f1)
            result = dict()
            result['version'] = "MINDsLab"
            result['data'] = list()

            for data in doc["data"]:
                pre_result = dict()
                pre_result['paragraphs'] = list()

                doc_key = data.keys()
                c = re.search("(?<=['])(.*)(?=['])", str(doc_key))
                d = c.group()
                logger.info("doc_key: %s", d)

                qas_list = list()
                for qa in data[d]['qas']:
                    qas_dict = dict()
                    self.start_id += 1
                    q_id = self.start_id
                    question = qa['question']
                    question = question.replace("\n", "")
                    # print(question)
                    level = str(qa['level']).split(" ")[2]
                    text = qa['answer'][0]['text']
                    answer_start = qa['answer'][0]['answer_start']
                    answer_end = qa['answer'][0]['answer_end']
                    qas_dict = {'id': q_id, 'question': question, 'question_level': level, 'question_en': '',
                                'question_tagged': '',
                                'questionType': '', 'questionFocus': '', 'questionSAT': '', 'questionLAT': '',
                                'lawName': '', 'answers': list()}
                    qas_list.append(qas_dict)

                    qas_dict['answers'].append(
                        {'text': text, 'answer_start': answer_start, 'answer_end': answer_end,
                         'text_en': '', 'text_tagged': '', 'text_syn': ''})

                data_dict = dict()
                public_date = data[d]['공포일자']
                article_content = data[d]['조내용']
                statute_code = data[d]['법령코드']
                document_id = data[d]['문서ID']
                article_no = data[d]['조번호']
                article_title = data[d]['조제목']
                belong_title = data[d]['소속제목']
                belong_no = data[d]['소속번호']
                law_name = data[d]['법령명']
                law_written_in_q = data[d]['메모']  # 0724추가

                data_dict['qas'] = list()
                data_dict['qas'] = qas_list

                data_dict['context_id'] = document_id
                # 추가
                # data_dict['법령코드'] = statute_code
                # data_dict['공포일자'] = promulgate
                # data_dict['소속번호'] = belong_no
                # data_dict['소속제목'] = belong_title
                # data_dict['조번호'] = article_no
                # data_dict['조제목'] = article_title
                # 추가 끝

                data_dict['context'] = article_content
                data_dict['context_en'] = ""
                data_dict['context_tagged'] = ""
                data_dict['law_written_in_q'] = law_written_in_q

                pre_result['paragraphs'].append(data_dict)
                pre_result['title'] = law_name

                result['data'].append(pre_result)

            # f2 = open("/home/msl/ys/cute/data/cw_law/20190614법률MRC구축_최종데이터/json/sum2.json", 'w', encoding='utf-8')
            f2 = open(os.path.join(self.output_dir, "파일럿과1차sum2.json"), "w", encoding='utf-8')
            json.dump(result, f2, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    c = json_merge_and_count()
    c.refine()