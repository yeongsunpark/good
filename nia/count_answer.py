#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-03-06

import os
import logging
import re

# f2 = open("/home/msl/ys/cute/nia/no_marker/error_checker.tsv","w")
# f3 = open("/home/msl/ys/cute/nia/no_marker/normal_checker.tsv","w")


for f1 in os.listdir("/home/msl/ys/cute/nia/yes_marker"):
    if "일반Q&A본문표시" not in f1:
        continue
    print(f1)
    # creator = f.split("_")[2].split(".")[0]
    creator = "전체"
    logging.error(creator)
    f2_list = []
    f3_list = []

    # f = open("no_checker.tsv", "r")
    with open(os.path.join("/home/msl/ys/cute/nia/yes_marker", f1), "r") as f:
        t = ""
        l = ""
        num = 1
        header = True

        for line in f:
            item = line.split("\t")
            # print (line)
            if header:
                header = False
                continue

            if item[1] != "":  # 만약에 공백이 아니라면
                content = item[1]  # 컨텐츠에 본문 넣고
                answer = item[4].replace("\n", "")
                l = item[1]  # 후를 위해 l에 컨텐츠를 넣어놓음.
                t = item[0]

            elif item[1] == "":  # 만약에 공백이라면
                content = l  # 컨텐츠에 위에 넣은 l 을 넣고.
                # print (content)
                answer = item[4].replace("\n", "")
            else:
                print(line)
                break

            m_answer = "|" * 5 + answer + "|" * 5
            a = content.count(m_answer)  # 컨텐츠에서 m_answer 가 몇 개 있는지 찾을 건데

            if a != 1:  # 일이 아니면 ㅋㅋㅋ 오류야!!!
                print (line)

                f2_list.append([t, str(num), item[2], item[3], answer, l, str(a)])
                # f2.write("\t".join([t, str(num), item[2], item[3], item[4], l, str(a)]))
                # f2.write("\n")
                with open(
                        os.path.join("/home/msl/ys/cute/nia/yes_marker/", "본문표시_error_{}.tsv".format(creator)),
                        'w', encoding='utf8') as f2:
                    for fl in f2_list:
                        f2.write("\t".join(fl))
                        f2.write("\n")

                # break

            elif a == 1:
                try:
                    a_location = content.index("{}{}{}".format("|" * 5, answer, "|" * 5))
                    markers = list()
                    for m in ["|"]:
                        markers += [match.start() for match in re.finditer(re.escape(m * 5), content)]
                    a_location -= len([x for x in markers if x < a_location]) * 5
                    a_para_strip = content
                    for m in ["|"]:
                        a_para_strip = a_para_strip.replace(m * 5, "")
                    new_answer = a_para_strip[a_location:a_location + len(answer)]
                    try:
                        assert (answer == new_answer)
                    except AssertionError:
                        print ("no match")
                        print (line)
                        exit()
                except ValueError as e:
                    print (line)
                    exit()

                b = a_location
                m_context = content.replace("|" * 5, "")
                m_context = m_context[:b] + "|" * 5 + answer + "|" * 5 + m_context[b + len(answer):]
                f3_list.append(
                    [t, m_context, str(num), item[3], answer, "", "", l.replace("|" * 5, ""), str(b),
                     str(b + len(answer))])  # common_tsv 를 위해 수정
                with open(
                        os.path.join("/home/msl/ys/cute/nia/yes_marker/", "본문표시_normal_{}.tsv".format(creator)),
                        'w', encoding='utf8') as f3:
                    for fl in f3_list:
                        f3.write("\t".join(fl))
                        f3.write("\n")
            else:
                print(line)
                break
            num += 1

