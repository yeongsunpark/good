#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-12

import os, sys
import logging
sys.path.insert(0,'..')
import ys_logger
logger = logging.getLogger('root')

def comp_with_ori(ind, q_id, context, question, answer, mod_question, mod_answer, mod_context, remarks):
    # 원본 가져오기
    flag = False
    with open ("/home/msl/ys/cute/data/sams2/entity_200_all_v2.txt", "r") as f2:
        for line2 in f2:
            item2 = line2.strip().split("\t")
            q_id2 = item2[0]
            context2 = item2[1]
            question2 = item2[2]
            answer2 = item2[3]

            # q_id 에 해당하는 아이디를 원본에서 찾으면
            if q_id == q_id2:
                flag = True

                # 본문의 마커가 바뀐 것은 정답 수정이기 때문에 본문들에서 마커 지움 + 띄어쓰기도 지움.
                context_ori1 = context.replace("[","").replace("]","")
                context_ori2 = context2.replace("[","").replace("]","")
                context = context_ori1.replace(" ","")
                context2 = context_ori2.replace(" ","")

                # 본문/질문/답 (편의를 위해 eval 사용했고 가독성 떨어짐...)
                for kind in ["context", "question", "answer"]:
                    if eval(kind) != eval("%s2" % kind): # 본문/질문/답이 수정되었는데
                        if eval("mod_%s" % kind) == "":  # 체커가 안 되어 있다면
                            # logger.error("No Marker At Line%s\nq_id%s\n%s1:%s\n%s2:%s"%(ind, q_id, kind, eval(kind), kind, eval("%s2"%kind)))
                            logger.error("Need %s Checker At Line%s" % (kind, ind))
                            logger.error("q_id: %s" % q_id)
                            if kind == "context":
                                logger.error("%s1: %s" % (kind, context_ori1))
                                logger.error("%s2: %s" % (kind, context_ori2))
                            else:
                                logger.error("%s1: %s" % (kind, eval(kind)))
                                logger.error("%s2: %s" % (kind, eval("%s2" % kind)))

                            exit()

                    else:  # 본문/질문/답이 수정되지 않았는데
                        if eval("mod_%s" % kind) !="":  # 체커가 되어 있다면
                            logger.error("Delete %s Checker At Line%s" %(kind, ind))
                            logger.error("q_id: %s" % q_id)
                            logger.error("%s1:%s" % (kind, eval(kind)))
                            logger.error("%s2:%s" % (kind, eval("%s2" % kind)))
                            exit()
                
                """
                # 본문
                context = context.replace("[[[[[","").replace("]]]]]","")
                context2 = context2.replace("[[[[[","").replace("]]]]]","")
                if context != context2:
                    if mod_context == "":
                        logger.error("Line%s: Context. q_id:%s", ind, q_id)
                        exit()
                else:
                    if mod_context != "":
                        logger.error("Line%s: Context. q_id:%s", ind, q_id)
                        exit()
                # 질문
                if question != question2:
                    if mod_question == "":
                        logger.error("Line%s: Question, q_id:%s", ind, q_id)
                        exit()
                else:
                    if mod_question != "":
                        logger.error("Line%s: Question, q_id:%s", ind, q_id)
                # 답
                if answer != answer2:
                    if mod_answer == "":
                        logger.error("Line%s: Answer, q_id:%s", ind, q_id)
                else:
                    if mod_answer != "":
                        logger.error("Line%s: Answer, q_id:%s", ind, q_id)
                """

        if not flag:
            # q_id 가 원본에 없는 경우.
            logger.error("Line%s: No q_id in Origin. q_id:%s, q_id2:%s", ind, q_id, q_id2)
            exit()

def find_ori(q_id):
    # 원본 가져오기
    flag = False
    with open ("/home/msl/ys/cute/data/sams2/entity_200_all_v2.txt", "r") as f2:
        for line2 in f2:
            item2 = line2.strip().split("\t")
            q_id2 = item2[0]
            context2 = item2[1]
            question2 = item2[2]
            answer2 = item2[3]

            # q_id 에 해당하는 아이디를 원본에서 찾으면
            if q_id == q_id2:
                flag = True

                return question2, answer2, context2


if __name__ == '__main__':
    # comp_with_ori("1", "entity_500_gen_0", "본문", "질문", "답", "", "", "", "")
    print (find_ori("entity_500_gen_19988"))
    logger.setLevel("DEBUG") # INFO
    logger.addHandler(ys_logger.MyHandler())
    logger.info("All finished")