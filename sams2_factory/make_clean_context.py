#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-20

import os, sys
import logging
import json
sys.path.insert(0,'..')
import ys_logger
logger = logging.getLogger('root')

# find index and make clean context
def make_clean_context(q_id, context_ori, answer):
    try:
        a_location = context_ori.index("{}{}{}".format("[" * 5, answer, "]" * 5))
        fin_answer = context_ori[a_location+5:a_location+5+len(answer)]  # 뽑아낸 answer
        fin_context = context_ori[:a_location]+answer+context_ori[a_location+5+len(answer)+5:]  # fin_context/ 마커를 지운 본문

    except ValueError as e:
        logger.error("q_id:%s, %s" %(q_id, e))
        logger.error("context_ori:%s"%context_ori)
        logger.error("answer:%s"%answer)
        exit()
    if answer == fin_answer == fin_context[a_location:a_location+len(answer)]:
        return fin_context, a_location
    else:
        logger.error("q_id:%s"%q_id)
        logger.error("answer:%s"%answer)
        logger.error("fin_answer:%s"%fin_answer)
        logger.error("extract_answer%s"%fin_context[a_location:a_location+len(answer)])
        exit()

if __name__ == '__main__':
    print(make_clean_context("11", "나는 안녕라고 [[[[[[[말]]]]]]]함", "말"))