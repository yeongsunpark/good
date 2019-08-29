#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-28


# q_id 별로 나눠서 저장
def tsv_cut(file_name, q_start, q_end):
    f_in = open("/home/msl/ys/cute/data/sams2/entity_200_all_v2_ascend.txt", "r")
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
    a = tsv_cut("현주", "entity_500_gen_0", "entity_500_gen_1533") # 단, 제일 끝은 하나 크게 하기.