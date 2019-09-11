#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-09-02

import sys, os
import json
import re
import logging

class json_merge():
    def __init__(self):
        self.input_dir = "/home/msl/ys/cute/data/wiki_0902/result_SR"
        self.output_dir = "/home/msl/ys/cute/data/wiki_0902/json"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.start_id = 19000000
        self.version = "MINDsLab_2019"
        self.creator = "MINDsLab"

    def merge(self):
        result = dict()
        result['version'] = 1
        result['creator'] = "MINDs Lab."
        result['data'] = list()
        for f1 in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, f1), "r") as f:
                json_data1 = json.load(f)
                result['data'].append(json_data1)
        with open (os.path.join(self.output_dir, "낱개를하나로.json"), "w") as f2:
            json.dump(result, f2, indent=2, ensure_ascii=False)

    def main(self):
        with open(os.path.join(self.output_dir,  "낱개를하나로.json"), "r", encoding='utf-8') as f1:
            docc = json.load(f1)
            result = dict()
            result['version'] = self.version
            result['creator'] = self.creator
            result['data'] = list()

            for doc in docc["data"]:
                pre_result = dict()
                pre_result['paragraphs'] = list()

                qas_list = list()
                qas_dict = dict()
                self.start_id +=2
                q_id = self.start_id
                # question1
                question1 = doc["question1"]
                text = doc["answer"]
                answer_start = doc["answerDragStartOffset"]
                answer_end = doc["answerDragEndOffset"]
                qas_dict1 = {'id':q_id-1, 'question':question1, 'question_en':'',
                            'question_tagged':'', 'questionType':'', 'questionFocus':'', 'questionSAT':'', 'questionLAT':'',
                            'answers':list()}
                qas_list.append(qas_dict1)
                qas_dict1['answers'].append({'text':text, 'answer_start':answer_start, 'answer_end':answer_end,
                                            'text_en':'', 'text_tagged':'', 'text_syn':''})

                # question2
                question2 = doc["question2"]
                qas_dict2 = {'id':q_id, 'question':question2, 'question_en':'',
                            'question_tagged':'', 'questionType':'', 'questionFocus':'', 'questionSAT':'', 'questionLAT':'',
                            'answers':list()}
                qas_list.append(qas_dict2)
                qas_dict2['answers'].append({'text':text, 'answer_start':answer_start, 'answer_end':answer_end,
                                            'text_en':'', 'text_tagged':'', 'text_syn':''})

                data_dict = dict()
                data_dict['qas']= list()
                data_dict['qas']= qas_list
                data_dict['context_id'] = doc['paragraphID']
                data_dict['context'] = doc['content']
                data_dict['context_en'] = ""
                data_dict['context_tagged'] = ""

                pre_result['paragraphs'].append(data_dict)
                pre_result['title'] = doc['title']

                result['data'].append(pre_result)

            f2 = open(os.path.join(self.output_dir, "final.json"), "w", encoding='utf-8')
            json.dump(result, f2, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    c = json_merge()
    c.main()
    c.main()