#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-28


# q_id 별로 나눠서 저장
def tsv_cut(file_name, q_start, q_end):
    f_in = open("/home/msl/ys/cute/data/sams2/random_questions_from_m4_5_to_6_ascend.txt", "r")
    f_out = open("/home/msl/ys/cute/data/sams2/" + file_name + ".txt", "w")

    flag = False

    for line in f_in:
        q_id = line.split("\t")[0]
        if q_start == q_id:
            flag = True
        elif q_end == q_id:
            break

        if flag:
            f_out.write(line)

    f_out.close()
    f_in.close()
    return "finish"

if __name__ == '__main__':
    a = tsv_cut("랜덤_1", "random_questions_38956", "random_questions_1710") # 단, 제일 끝은 하나 크게 하기.  # 2133 ~ 3145
    a = tsv_cut("랜덤_2", "random_questions_24570", "random_questions_28289") # 단, 제일 끝은 하나 크게 하기.  # 3146 ~ 4665
    a = tsv_cut("랜덤_3", "random_questions_89211", "random_questions_92848") # 단, 제일 끝은 하나 크게 하기.  # 4656 ~ 6220
    a = tsv_cut("랜덤_4", "random_question2_62664", "random_question2_65000") # 단, 제일 끝은 하나 크게 하기.  # 6221 ~ 8002
    a = tsv_cut("랜덤_5", "random_question2_16160", "random_question2_17679") # 단, 제일 끝은 하나 크게 하기.  # 6221 ~ 8002