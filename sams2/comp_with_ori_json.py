#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-20

import os, sys
import logging
import json
sys.path.insert(0,'..')
import ys_logger
logger = logging.getLogger('root')

# 원본 json 과 비교하기.
def comp_with_ori_json(q_id, source1, source_link1):
    # 원본 가져오기
    flag = False
    with open("/home/msl/ys/cute/data/sams2/save/entity_and_random_question.json", "r") as f2:
        json_data1 = json.load(f2)
        for data in json_data1["data"]:
            for para in data["paragraphs"]:
                for qas in para["qas"]:
                    id = qas["id"]
                    for ans in qas["answers"]:
                        confidence = ans["confidence"]
                        source = ans["source"]
                        source_link = ans["source_link"]
                        if id == q_id and source1 == source and source_link1 == source_link:
                            return confidence
                            # flag = True
                            # for ans in qas["answers"]:
                                # if confidence and source and source_link:
                                    # return confidence

        if not flag:
            logger.error("1_id: %s, 찾을 수 없음"%q_id)
            logger.error("source1: %s"%source1)
            logger.error("source2: %s" %source)
            logger.error("source_link1: %s"%source_link1)
            logger.error("source_link2: %s" % source_link)
            exit()

if __name__ == '__main__':
    print(comp_with_ori_json("entity_500_gen_8002", "[Wiki] 로버트 W. 펑크", "https://ko.wikipedia.org/wiki?curid=2280224"))