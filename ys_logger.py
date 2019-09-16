#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-24

import logging
# custom_logger.py 와 구분을 위해 이름 바꿈

class MyHandler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >>> %(message)s'
        fmt_date = '%Y-%m-%d_%T %Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)
        # logging.basicConfig(filename='/home/msl/ys/good/sams1/output.log', level=logging.ERROR)
