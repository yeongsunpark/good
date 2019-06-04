#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-03

import os, sys
import json
import re

sys.path.append(os.path.abspath('/home/msl/ys/good/mrc_utils'))
from morp_analyze_my import NLPAnalyzer

class Sim:
    def __init__(self):
        self.nlp_analyze = NLPAnalyzer()
        self.input_dir = "/home/msl/ys/cute/data/cw0530/20190531_마인즈랩법률결과_1966"
        self.output_dir = "/home/msl/ys/cute/data/cw0530/result_morp"

    def main(self):
        f2 = open(os.path.join(self.output_dir, "recall.txt"), 'w', encoding='utf-8', newline='')
        for f in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, f), 'r', encoding='utf-8') as f1:
                doc = json.load(f1)
            doc_key = doc.keys()
            c = re.search("(?<=['])(.*)(?=['])", str(doc_key))
            d = c.group()
            # f2 = open(os.path.join(self.output_dir, f.split(".")[0] + ".txt"), 'w', encoding='utf-8', newline='')

            article_content = doc[d]['조내용']
            context_mp = self.nlp(article_content)
            context_f = filt(context_mp)

            for qa in doc[d]['qas']:
                question = qa['question']
                question = question.replace("\n", "")
                level = str(qa['level']).split(" ")[2]
                question_mp = self.nlp(question)
                question_f = filt(question_mp)
                # f2.write("\t".join([str(cnt(context_f, question_f)), level, "\n"]))
                if level == "상":
                    sang = question
                    sang_cnt = cnt(context_f, question_f)
                elif level == "중":
                    joong = question
                    joong_cnt = cnt(context_f, question_f)
                elif level == "하":
                    ha = question
                    ha_cnt = cnt(context_f, question_f)

            if sang_cnt <= joong_cnt <= ha_cnt:
                continue
            else:
                print (f)
                f2.write("".join([sang, "\t", str(sang_cnt), "\n", joong, "\t", str(joong_cnt), "\n", ha, "\t", str(ha_cnt), "\n"]))
                f2.write("\n")
        f2.close()

    
    def nlp(self, sentence):
        processed_ans = self.nlp_analyze.get_result_morp_list(sentence)
        return processed_ans

def filt(morp):
    a = []
    for m in morp:
        if "/nn" in m or "/vv" in m:
            a.append(m)
    return a

def cnt(context, question):
    i = 0
    for q in question:
        if q in context:
            i +=1
    return i/len(question)

if __name__ == "__main__":
    j = Sim()
    j.main()