#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-08

import os, sys
import logging
import re
sys.path.insert(0,'..')
import ys_logger
logger = logging.getLogger('root')

# 마커가 다섯개인지 아닌지 확인.
def marker_checker(ind, q_id, context, answer):
    open_mark = context.count("[")
    close_mark = context.count("]")
    if open_mark == 5 and close_mark == 5:  # 총 마커의 개수가 다섯개씩인데
        if context.count("[[[[[") != 1 or context.count("]]]]]") != 1: # 다섯개가 주르륵 있지 않다면 오류.
            logger.error("Fewer Marker At Line%s, q_id:%s", ind, q_id)
            exit()
    elif answer == "":  # 답 없는 질문인데
        if context.count("[[[[[") == 1 or context.count("]]]]]") == 1:  # 마커가 다섯개 씩 있다면 오류.
            logger.error("There Is A Marker At Line%s, q_id:%s is No Answer Type", ind, q_id)
            exit()
    else:  # 마커가 여섯개 이상 주르륵이면 오류.
        p = re.compile('(\[{5,}.*\]{6,})|(\[{6,}.*\]{5,})')
        if p.search(context):
            logger.error("Many Marker At Line:%s, q_id:%s, open_marker:%s, close_marker:%s", ind, q_id, open_mark, close_mark)
            exit()

if __name__ == '__main__':
    marker_checker("1", "본문")
    logger.setLevel("DEBUG") # INFO
    logger.addHandler(ys_logger.MyHandler())
    logger.info("All finished")