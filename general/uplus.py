# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import re

class abc():
    def __init__(self):
        self.f = 'uplus3.tsv'
        # self.f2 = open('uplus3_result.txt', 'w')
        self.data = []

    def ab(self):
        f = open(self.f, 'r')
        line = f.readline()
        item = line.split("\t")
        print (len(item))
        f.close()
        return len(item)

    def abcdefg(self, number):
        for i in range(1, int(number)):
            with open(self.f, 'r') as f:  # 계속 열어 줘야해서 이렇게 씀. 안 그러면 한 번밖에 안 열림.
                for line in f:
                    item = line.strip("\n").split("\t")
                    if item[i] != "":
                        # self.f2.write("[[")
                        self.f2.write(item[0])
                        self.f2.write(";;")
                        # self.f2.write("]]")
                        self.f2.write(item[i])
                        self.f2.write(";;;")
                    else:
                        print ("check")
                #self.f2.write("\n")
                self.f2.write("\n")
        return ()

    def abcd(self, number):
        for i in range(1, int(number)):
            with open(self.f, 'r') as f:  # 계속 열어 줘야해서 이렇게 씀. 안 그러면 한 번밖에 안 열림.
                for line in f:
                    item = line.strip("\n").strip("\n").split("\t")
                    # if item[i] != "" and item[0] !="타사비교" and item[0] !="충분도" and item[0] !="프로세스"and item[0] !="담당자":
                    if item[i] != "" and item[i] !="\n" and (item[0] =="NO." or item[0] =="카테고리1" or item[0] =="카테고리2" or item[0] =="카테고리3" or item[0] == "항목명"\
                            or item[0] == "필수" or item[0] == "개요" or item[0] == "상세내용" or item[0] == "Script & SMS"):
                        # self.f2.write(item[0])
                        self.data.append(item[0])
                        # self.f2.write(";;")
                        self.data.append(";;")
                        # self.f2.write(item[i])
                        self.data.append(item[i])
                        # self.f2.write(";;;")
                        self.data.append(";;;")
                    else:
                        # print (item[0], item[1])
                        pass
                #self.f2.write("\n")
                #self.f2.write("\n")
                self.data.append("\n")
        self.f2.write("".join(self.data))
        return ()

    def abcde_bak(self):
        f2 = open("uplus3_result.txt", 'r')
        for j in f2:
            j2 = j.split(";;;")
            for a in range (len(j2)):
                # print (j2[a])
                if j2[a].startswith("필수"):
                    j3 = j2[a].split("///")
                    for b in range(len(j3)):
                        # print (j3[b])
                        if "[핵심정보]" in j3[b]:
                            print (j3[b])
                        """
                        j3[b] = j3[b].replace("[핵심정보]", "[핵심정보];;")
                        j3[b] = j3[b].replace("TIP]", "TIP];;")
                        j3[b] = j3[b].replace("알아두기]", "알아두기];;")
                        print (j3[b])
                        """
        return ()
    def abcde(self):
        # aa = re.compile('.*■.*-*.*')
        # f2 = open("uplus_result.txt", "r")
        f2 = open("C54.txt", "r")
        f3 = open("uplus_result2.txt", "w")
        for j in f2:
            j2 = j.split("\t")
            f3.write(j2[0])
        """
        for line in f2:
            # line = line.replace(" \n", "\n")
            line = re.sub(" \n", "\n", line)
            line = re.sub("^ +", "", line)
            # print (line)
            f3.write(line)
        """


if __name__ == "__main__":
    a = abc()
    # b = a.ab()
    # c = a.abcd(b)  # b의 결과 값인 item 수를 c에 넣어준다.
    d = a.abcde()
