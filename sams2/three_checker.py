#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-08

import os, sys
import logging
sys.path.insert(0,'..')
import ys_logger
from comp_with_ori import find_ori
logger = logging.getLogger('root')

def three_checker(ind, q_id, classify, context_ori, question, answer, mod_question, mod_answer, mod_context):
    # 숫자가 아닌 게 들어 왔는지 확인 (문자, 공백 등)
    try:
        classify = int(classify)
    except ValueError as e:
        logger.error("Line%s, q_id:%s, %s", ind, q_id, e)
        exit()

    # 범위 외 숫자가 들어 왔는지 확인
    if classify != 1 and classify != 2 and classify != 3 and classify != 4:
        logger.error("Line%s, q_id:%s, Invalid classify:%s ", ind, q_id, classify)
        exit()

    # 분류 1번인데 체커 했을 경우 확인
    if classify == 1:
        if mod_question == "" and mod_answer == "" and mod_context == "":
            logger.debug("Line%s, q_id:%s", ind, q_id)
        else:
            logger.error("Delete Checker At Line%s, q_id:%s, mod_question:%s, mod_answer:%s, mod_context:%s", ind, q_id, mod_question, mod_answer, mod_context)
            ori = find_ori(q_id)  # return Q, A, C
            if mod_question != "":
                logger.error("question1:%s", question)
                logger.error("question2:%s", ori[0])
            elif mod_answer != "":
                logger.error("answer1:%s", answer)
                logger.error("answer2:%s", ori[1])
            else:
                logger.error("context_ori1:%s", context_ori)
                logger.error("context_ori2:%s", ori[2])
            exit()

    # 분류 1번 아닌데 체커 안 했을 경우 확인
    elif classify != 1:
        if mod_question != "" or mod_answer != "" or mod_context != "":
            logger.debug("Line%s q_id:%s", ind, q_id)
        else:
            logger.error("Need Checker At Line%s, q_id:%s, class:%s, m_q:%s, m_a:%s, m_c:%s", ind, q_id, classify, mod_question, mod_answer, mod_context)
            ori = find_ori(q_id)
            logger.error("question1:%s", question)
            logger.error("question2:%s", ori[0])
            logger.error("answer1:%s", answer)
            logger.error("answer2:%s", ori[1])
            logger.error("context_ori1:%s", context_ori)
            logger.error("context_ori2:%s", ori[2])
            exit()

if __name__ == '__main__':
    three_checker("1", "뮻", "", "", "")
    logger.setLevel("DEBUG") # INFO
    logger.addHandler(ys_logger.MyHandler())
    logger.info("All finished")