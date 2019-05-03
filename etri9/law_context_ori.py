#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-04-29

import os, sys, logging
import json
import re
sys.path.append(os.path.abspath('..'))
import ys.good.ys_logger as ys_logger

logger = logging.getLogger('root')
logger.setLevel("INFO")
logger.addHandler(ys_logger.MyHandler())
logger.info("Finish setting logger")

input_dir = "/home/msl/ys/cute/data/law"
logging.basicConfig(filename='%s/example.log'%input_dir,level=logging.INFO,
                    format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >>> %(message)s')


revision = re.compile(  # '<개정 *\d+[.] *\d+[.] *\d+[.][,] *\d+[.] *\d+[.] \d*[.]>|'
    '<개정( *\d+[.] *\d+[.] *\d+[.][,])+ *\d+[.] *\d+[.] \d*[.]*>|'
    '<(개정|신설) *\d+[.] *\d+[.] *\d+[.]([,] *\d+[.] *\d+[.] *\d+[.])*>|'
    '[[](전문개정|제목개정|본조신설) *\d+[.] *\d+[.] * \d+[.]]|'
    '[[]시행일 *[:] *\d+[.] *\d+[.] *\d+[.]*]|'
    '[[]제\d+조(의\d)*에서 이동.*]|'
    '[[]종전 제\d+조(의\d+)*는 제\d+조(의\d+(으)*)*로 이동.*]|'
    '제\d*. 삭제 *<\d+[.]* \d+[.]* \d+[.]>|'  # 9/17 add
    '제\d*조의\d*. 삭제 *<\d+[.]* \d+[.]* \d+[.]>|'  # 9/17 add
    '[제\d조 및 ]*제\d*조 생략|'  # 9/17 modi
    '제\d*조부터 제\d조*까지 생략|'  # 9/17 add
    '(제\d조[(]시행일[) ])*이 법은 (.)*부터 시행한다[.].*|'  # 9/17 add
    '. 삭제 *<\d+[.]* \d+[.]* \d+[.]>|'
    '[[]\d+[.] *\d+[.] *\d+[.] *법률 제\d+.*삭제함.]|'
    '[[]법률 제\d+호[(]\d+[.] *\d+[.] *\d+[.][)].*규정에 의하여 .*\d일까지 유효함]|'
    '<단서 생략>|'
    '<개정 *\d+[.] *\d+[.] *\d+>')



for f in os.listdir(input_dir):
    if "txt" not in f:
        continue
    else:
        with open(os.path.join(input_dir, f), "r") as f1:
            logger.info("open file: %s" % f)
            d = f1.readlines()
            data = '{"1":['
            for i in range(len(d)):
                data += d[i]
            data = data.replace("}", "},")
            data += "]}"
            data = data.replace("\n", "")
            data = data.replace("  ", "")
            data = data.replace("]},]}", "]}]}")

        with open((os.path.join(input_dir, "output/{}_result.json").format(f.split(".")[0])), "w") as f2:
            f2.write(data)
            logger.info("save file: %s" % f)
        # os.system("mv {input_dir}/{file} {input_dir}/used/".format(input_dir=input_dir, file=f))

        with open((os.path.join(input_dir, "output/{}_pretty_result.json").format(f.split(".")[0])), "w") as f3:
            """
            new_dict = {}
            data_dict = json.loads(data)
            for d in data_dict:
                for i in range(len(data_dict[d])):  # 11
                    new_words = ""
                    for item in data_dict[d][i]['조내용']:
                        if revision.search(item):
                            new = revision.sub("", item)
                            new_words+= new
                        else:
                            new_words+= item

                        data_dict[d][i]['조내용'] = new_words
                        new_dict[d] = data_dict[d]
            data_dict = json.dumps(new_dict[d], ensure_ascii=False, indent = 2)
            f3.write(data_dict)
            """
            result = dict()
            result['0'] = list()
            print (result)
            data_dict = json.loads(data)
            for d in data_dict:
                for i in range(len(data_dict[d])):
                    new_words = ""
                    for item in data_dict[d][i]['조내용']:
                        if revision.search(item):
                            new = revision.sub("", item)
                            new_words+= new
                        else:
                            new_words+= item
                        data_dict[d][i]['조내용'] = new_words
                    if len(new_words) >= 50:
                        result['0'].append(data_dict[d][i])
                data_dict = json.dumps(result, ensure_ascii=False, indent = 2)
                f3.write(data_dict)