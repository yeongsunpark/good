#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-08
import sys

def change_wh(wh):
    if wh == "언제" or wh == "과거" or wh == "when":
        return "work_when"
    elif wh == "어디서" or wh == "어디" or wh == "어디에" or wh == "어디서서" or wh == "where":
        return "work_where"
    elif wh == "누가" or wh == "누구"or wh == "who":
        return "work_who"
    elif wh == "무엇을" or wh == "무엇이" or wh == "무슨" or wh == "무엇" or wh == "무엇은" or wh == "뭐라고"\
            or wh == "우멋을" or wh == "무엇으로" or wh == "무얼을" or wh == "무어슬" or wh == "what":
        return "work_what"
    elif wh == "어떻게" or wh == "어떻계" or wh == "how":
        return "work_how"
    elif wh == "왜" or wh == "why":
        return "work_why"
    else:
        return ""

# 사용방법: python3 check_wh.py /home/msl/ys/cute/nia/smooth/new_normal_finish-sum2.txt
def check_wh():
    rd = dict()
    if len(sys.argv) == 1:
        # open_file = "/home/msl/ys/cute/nia/smooth/new_normal_finish-sum2.txt"
        print ("sys.argv error")
    else:
        open_file = sys.argv[1]
    with open(open_file, "r") as f:
        for line in f:
            item = line.strip().split("\t")
            if len(item) == 10:
                wh = item[6].strip()
            elif len(item) == 4 and "asdf.tsv" in sys.argv[1]:
                wh = item[2]
            elif len(item) == 2 and "asdf.tsv" in sys.argv[1]:
                wh = item[0]
            else:
                print (line)
                break
            if wh != "언제" and wh != "어디서" and wh != "누가" and wh != "무엇을" and wh != "어떻게" and wh != "왜":
                if wh in rd:
                    rd[wh] += 1
                else:
                    rd[wh] = 1
    print(str(rd))

if __name__ == "__main__":
    check_wh()
