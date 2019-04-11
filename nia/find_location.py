#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-03-25

import re
def find_index(a_para, answer):
    try:
        a_location = a_para.index("{}{}{}".format("|" * 5, answer, "|" * 5))
        markers = list()
        for m in ["|"]:
            markers += [match.start() for match in re.finditer(re.escape(m * 5), a_para)]
        a_location -= len([x for x in markers if x < a_location]) * 5
        a_para_strip = a_para
        for m in ["|"]:
            a_para_strip = a_para_strip.replace(m * 5, "")
        new_answer = a_para_strip[a_location:a_location + len(answer)]

        try:
            assert (answer == new_answer)
        except AssertionError:
            print ("assertionError")
            print(a_para + "\n" + answer)
            exit()
    except ValueError as e:
        print (a_para+"\n"+answer)
        exit()
    return a_location
