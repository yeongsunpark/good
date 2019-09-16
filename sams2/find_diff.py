#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-23

a = "안녕하세요"
b = "안녕해세요"
i = 0
j = 0
for aa, bb in zip(a, b):
    if aa == bb:
        i += 1
        continue
    else:
        print (a[i:])
        print (b[i:])
        break
"""
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
"""