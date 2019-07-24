#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-22

import os, sys
import json
import re
import logging

class Find():
    def __init__(self):
        self.pwd = "/home/msl/ys/cute/data/re_law"
        self.want = "/want"
        self.dupli = "/dupli"
        self.final = "/파일럿과1차"

    def duplication(self):
        dup_list = ["167", "170", "181", "193", "200", "205", "206", "208", "209", "212", "214", "216", "218", "219", "221", "225", "243", "244"]
        input_dir = self.pwd+self.want
        output_dir = self.pwd+self.dupli
        for fl in os.listdir(input_dir):
            for dl in dup_list:
                my_regex = r"^" + re.escape(dl) + r"[_]"
                if re.search(my_regex,fl):
                    ind = input_dir.replace("(", "\(").replace(")", "\)")
                    # os.system ("cp %s/%s %s" % (str(ind), str(fl), str(output_dir)))
                    os.system ("cp {ind}/{fl} {outd}".format(ind = ind, fl = fl, outd = output_dir))
                    # os.system("mv %s/%s %s/want_%s" % (str(output_dir), str(fl), str(output_dir), str(fl)))
                    os.system("mv {outd}/{fl} {outd}/want_{fl}".format(outd = output_dir, fl = fl))

    def all(self):
        input_list = ["답과3가지질문만들기-1차(1474건)", "답과3가지질문만들기-1차(1474건)2",
                      "답과3가지질문만들기-파일럿(374건)", "답과3가지질문만들기-파일럿(374건)2", "dupli_corrected"]
        output_dir = self.pwd + "/" + self.final
        for input_element in input_list:
            input_dir = self.pwd+"/"+input_element
            print (input_dir)
            if "1차" in input_dir:
                order = "1_"
            elif "파일럿" in input_dir:
                order = "0_"
            else:
                order = ""

            for fl in os.listdir(input_dir):
                ind = input_dir.replace("(", "\(").replace(")", "\)")

                os.system("cp {ind}/{fl} {outd}".format(ind=ind, fl=fl, outd=output_dir))
                if order == "1_" or order == "0_":
                    os.system("mv {outd}/{fl} {outd}/{order}{fl}".format(outd=output_dir, fl=fl, order = order))

if __name__ == "__main__":
    c = Find()
    c.all()