#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-03

context = ['제/xpn', '1/sn', '조/nnb', '(/ss', '목적/nng', ')/ss', '이/mm', '법/nng', '은/jx', '희귀/nng', '질환/nng', '의/jkg', '예방/nng', ',/sp', '진료/nng', '및/maj', '연구/nng', '등/nnb', '에/jkb', '관/nng', '하/xsv', 'ㄴ/etm', '정책/nng', '을/jko', '종합/nng', '적/xsn', '으로/jkb', '수립/nng', 'ㆍ/sp', '시행/nng', '하/xsv', '어/ec', '희귀/nng', '질환/nng', '으로/jkb', '인/nng', '하/xsv', 'ㄴ/etm', '개인/nng', '적/xsn', 'ㆍ/sp', '사회적/nng', '부담/nng', '을/jko', '감소/nng', '시키/xsv', '고/ec', ',/sp', '국민/nng', '의/jkg', '건강/nng', '증진/nng', '및/maj', '복지/nng', '향상/nng', '에/jkb', '이바지/nng', '하/xsv', '는/etm', '것/nnb', '을/jko', '목적/nng', '으로/jkb', '하/vv', 'ㄴ다/ef', './sf']

q1 = ['희귀/nng', '질환법/nng', '의/jkg', '목적/nng', '이/jks', '뭐/np', '이/vcp', '야/ef', '?/sf']
q2 = ['희귀/nng', '질환법/nng', '이/jks', '만들/vv', '어/ec', '지/vx', 'ㄴ/etm', '목적/nng', '이/jks', '뭐/np', '이/vcp', '야/ef', '?/sf']
q3 = ['희귀/nng', '질환법/nng', '을/jko', '왜/mag', '만들/vv', '었/ep', '어/ef', '?/sf']

a = []
for c in context:
    if "/nn" in c or "/vv" in c:
        a.append(c)
q = []
for c in q3:
    if "/nn" in c or "/vv" in c:
        q.append(c)
print (a)
print (q)

i = 0
for qq in q:
    if qq in a:
        print (qq)
        i +=1
print (i/len(q))