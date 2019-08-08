#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-08

import os, sys
import logging
sys.path.insert(0,'..')
import ys_logger
logger = logging.getLogger('root')

# 마커가 다섯개인지 아닌지 확인.
def marker_checker(ind, context):
    open_mark = context.count("[")
    close_mark = context.count("]")
    if open_mark == 5 and close_mark == 5:
        logger.debug("Line%s", ind)
    else:
        logger.error("Line:%s, open_marker:%s, close_marker:%s", ind, open_mark, close_mark)
        exit()

if __name__ == '__main__':
    marker_checker("1", "본문")
    logger.setLevel("DEBUG") # INFO
    logger.addHandler(ys_logger.MyHandler())
    logger.info("All finished")