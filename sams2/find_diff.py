#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-23

a = "박영선매니저님1987년 10월"
b = "박영선매니저님19888년 10월"

i = 0
j = 0
for aa, bb in zip(a, b):
    if aa == bb:
        i += 1
        continue
    else:
        start = i
for xx, yy in zip(a[::-1], b[::-1]):
    if xx == yy:
        j +=1
        continue
    else:
        end = j
print ("동일: %s"%a[:i])
print ("시트: %s"%a[i:-j+1])
print ("원본: %s"%b[i:-j+1])
print ("동일: %s"%a[-j+1:])