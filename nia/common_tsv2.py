#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-03-19

import find_location
import sys

header = True
result_list = []
number = 0
f = open("yes_marker/체커작업(2) - 시트1 (1).tsv", "r")
t = ""
c = ""
for line in f:
    line = line.replace("\n","")
    if header:
        header = False
        continue
    item = line.split("\t")
    if len(item) == 7:
        if item[0] != "":
            title = item[0]
            context = item[1]
            t = item[0]
            c = item[1]
        else:
            title = t
            context = c

        context_ori = context.replace("|||||", "")
        question = item[3]
        answer = item[4]
        # answer_s = context.find("|||||"+answer+"|||||")
        answer_s = find_location.find_index(context, answer)
        print (answer_s)
        answer_e = answer_s + len(answer)
        extract_answer = context_ori[answer_s:answer_e]
        number += 1
        if answer != extract_answer:
            result_list.append(
                [title, context, str(number), question, answer, "", item[6], context_ori, str(answer_s), str(answer_e)])
            print(answer_s)
            print(answer_e)
            print(answer)
            print(extract_answer)
            break
    else:
        print (len(item))

f.close()

f2 = open("yes_marker/체커작업(2) - 시트1 (1)_작업완료.tsv", "w")
print (len(result_list))
for r in result_list:
    f2.write("\t".join(r))
    f2.write("\n")