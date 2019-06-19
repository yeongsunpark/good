#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-30

import sys, os
import csv
import json
import re

json_data = open("post_pro.json", "r")
j = json_data.read()
j = json.loads(j)


class PostProcessing():
    def __init__(self):
        self.input_dir = j['input_dir']
        self.output_dir = j['output_dir']
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.full = True
        self.start_id = j['start_id']
        self.a = j['a']
        # read_json_path = '/home/msl/data/mrc/ko_wiki3/ko_mrc_v2_squad_pretty.json'
        # write_txt_path = 'etri_wiki_20_v2_ys.tsv'

    def main(self):
        for f in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, f), 'r', encoding='utf-8') as f1:
                print("file:", f)
                doc = json.load(f1)
            print ("file:", f)
            doc_key = doc.keys()
            # b = re.compile("(?<=['])(.*)(?=['])")
            # c = b.search(str(doc_key))
            c = re.search("(?<=['])(.*)(?=['])", str(doc_key))
            d = c.group()

            f2 = open(os.path.join(self.output_dir, str(self.a)+".txt"), 'w', encoding='utf-8', newline='')
            wr = csv.writer(f2, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')

            wr.writerow(["version", "", "", "", "", "MINDsLab_2019"])
            wr.writerow(["creator", "", "", "", "", "MINDsLab"])
            wr.writerow(["data"])


            promulgate = doc[d]['공포일자']
            article_content = doc[d]['조내용']
            statute_code = doc[d]['법령코드']
            document_id = doc[d]['문서ID']
            article_no = doc[d]['조번호']
            article_title = doc[d]['조제목']
            belong_title = doc[d]['소속제목']
            belong_no = doc[d]['소속번호']
            law_name = doc[d]['법령명']

            wr.writerow(["", "title", "", "", "", law_name])
            wr.writerow(["", "paragraphs"])
            wr.writerow(["", "", "context_id", "", "", document_id])
            if self.full:
                wr.writerow(["", "", "공포일자", "", "", promulgate])
                wr.writerow(["", "", "법령코드", "", "", statute_code])
                wr.writerow(["", "", "조번호", "", "", article_no])
                wr.writerow(["", "", "조제목", "", "", article_title])
                wr.writerow(["", "", "소속제목", "", "", belong_title])
                wr.writerow(["", "", "소속번호", "", "", belong_no])
            wr.writerow(["", "", "context", "", "", article_content])
            wr.writerow(["", "", "context_en"])
            wr.writerow(["", "", "context_tagged"])
            wr.writerow(["", "", "qas"])

            for qa in doc[d]['qas']:

                # q_id = qa['id']
                q_id = self.start_id
                self.start_id +=1
                question = qa['question']
                question = question.replace("\n","")
                level = str(qa['level']).split(" ")[2]
                wr.writerow(["", "", "", "id", "", q_id])
                wr.writerow(["", "", "", "question", "", question])
                wr.writerow(["", "", "", "난이도", "", level])
                wr.writerow(["", "", "", "question_en"])
                wr.writerow(["", "", "", "question_tagged"])
                wr.writerow(["", "", "", "questionType"])
                wr.writerow(["", "", "", "questionFocus"])
                wr.writerow(["", "", "", "questionSAT"])
                wr.writerow(["", "", "", "questionLAT"])

                text = qa['answer'][0]['text']
                answer_start = qa['answer'][0]['answer_start']
                answer_end = qa['answer'][0]['answer_end']
                # answer_end = 0
                wr.writerow(["", "", "", "answers"])
                wr.writerow(["", "", "", "", "text", text])
                wr.writerow(["", "", "", "", "text_en"])
                wr.writerow(["", "", "", "", "text_tagged"])
                wr.writerow(["", "", "", "", "text_syn"])
                wr.writerow(["", "", "", "", "answer_start", answer_start])
                wr.writerow(["", "", "", "", "answer_end", answer_end])

            f2.close()
            # break
            self.a+=1

if __name__ == "__main__":
    p = PostProcessing()
    p.main()