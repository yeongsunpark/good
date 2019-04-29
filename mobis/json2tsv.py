#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-29

import os, sys, json, csv

a = "/home/msl/ys/cute/nia/check/mobis/ko_nia_vnews_squad_train.json"
b = "/home/msl/ys/cute/nia/check/mobis/ko_nia_vnews_squad_train.tsv"

with open(a, "r", encoding="utf-8") as f1:
    json_data1 = json.load(f1)

f2 = open(b, "w", encoding="utf-8", newline="")
wr = csv.writer(f2, delimiter="\t")

result = []
for doc in json_data1['data']:
    title = doc['title']
    for p, t in zip(doc['paragraphs'], doc['title']):
        context = p['context']
        for qa in p['qas']:
            q_id = qa['id']
            question = qa['question']
            answer = qa['answers'][0]['text']
            answer_start = qa['answers'][0]['answer_start']
            result.append("\t".join([str(title), str(context), str(q_id), str(question), str(answer), str(answer_start)]))
for r in result:
    f2.write(r)
    f2.write("\n")
f2.close()