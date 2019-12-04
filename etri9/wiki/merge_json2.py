#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-02

import sys, os
import json
import re
import logging

class json_merge():
    def __init__(self):
        self.input_dir = "/home/msl/ys/cute/data/wiki_1203/check"
        self.output_dir = "/home/msl/ys/cute/data/wiki_1203/json"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.start_qid = 19000000
        self.start_pid = 0
        self.version = "MINDsLab_2019"
        self.creator = "MINDsLab"

    def merge(self):
        result = dict()
        result['version'] = 3
        result['creator'] = "MINDs Lab."
        result['data'] = list()
        for f1 in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, f1), "r") as f:
                json_data1 = json.load(f)
                result['data'].append(json_data1)
        with open (os.path.join(self.output_dir, "낱개를하나로.json"), "w") as f2:
            json.dump(result, f2, indent=2, ensure_ascii=False)

    def find_byte(self, context, start, end):
        byte_answer_start = len(context[:start].encode())
        byte_answer_end = len(context[:end].encode())
        # 아래와 같이 정답 text와 일치하는 지 여부 검사 필수
        """
        byte_paragraphs = paragraphs[‘context’].encode()
        byte_answer_text = byte_paragraphs[byte_answer_start:byte_answer_end]
        assert answers[‘text’] == byte_answer_text.decode(‘utf - 8’)
        """
        return byte_answer_start, byte_answer_end

    def main(self):
        with open(os.path.join(self.output_dir,  "낱개를하나로.json"), "r", encoding='utf-8') as f1:
            docc = json.load(f1)
            result = dict()
            result['version'] = self.version
            result['creator'] = self.creator
            result['data'] = list()

            for doc in docc["data"]:

                qas_list = list()
                self.start_qid +=1
                self.start_pid +=1
                q_id = self.start_qid
                p_id = "{0:0>6}".format(self.start_pid)
                # question1
                question1 = doc["question1"]
                text = doc["answer"]
                answer_start = doc["answerDragStartOffset"]
                answer_end = doc["answerDragEndOffset"]

                # question2
                question2 = doc["question2"]
                qas_dict2 = {'question_id':"q"+str(q_id), 'question_text':question2,
                             'question_text_syn':list(),
                            'answers_all':list(),
                             'paragraphs':list()}
                qas_list.append(qas_dict2)
                qas_dict2['question_text_syn'].append(question1)
                qas_dict2['answers_all'].append(text)

                # qas_dict2['paragraphs'].append({'id':"p"+str(p_id), 'title':doc['title'], 'context':doc['content'],
                qas_dict2['paragraphs'].append({'id':doc['paragraphID'], 'title':doc['title'], 'context':doc['content'],
                                                'answers':list()})

                byte_start, byte_end = self.find_byte(doc['content'], int(answer_start), int(answer_end))
                qas_dict2['paragraphs'][0]['answers'].append({"answer_text":text, "syllable_answer_start":int(answer_start), "syllable_answer_end":int(answer_end),
                                                            "byte_answer_start": byte_start, "byte_answer_end": byte_end})


                pre_result = dict()
                pre_result['questions'] = list()
                pre_result['questions'].extend(qas_list)
                # pre_result['questions'].append(qas_list)
                result['data'].append(pre_result)


            f2 = open(os.path.join(self.output_dir, "final3.json"), "w", encoding='utf-8')
            json.dump(result, f2, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    c = json_merge()
    c.merge()
    c.main()