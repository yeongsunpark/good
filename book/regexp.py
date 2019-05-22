#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-08
import re
p = re.compile('[a-z]+', )
m = p.match("python")
# m = re.match('[a-z]+', "python")

print ('매치된 문자열:', m.group())
print ('매치된 문자열의 시작 위치:', m.start())
print ('매치된 문자열의 끝 위치:', m.end())
print ('매치된 문자열의 (시작, 끝) 에 해당되는 튜플 리턴', m.span())

# 점과 숫자 사이 떼기
import re
# pattern1 = re.compile(r'([.])(\d)')
pattern1 = re.compile(r'(?P<period>[.])(\d)')  # name 사용
# space = pattern1.sub(r'\1 \2', '요거는.1번 떼보세요')
space = pattern1.sub(r'\g<period> \2', '요거는.1번 떼보세요')  # name 사용
print (space)

# 반복되는 문자 지우기
# pattern2 = re.compile(r'(.+)\1')
pattern2 = re.compile(r'(?P<word>.+)(?P=word)')  # name 사용
# clear = pattern2.sub(r'\1', "반반복복되되는 문자를 지지워워주세요요")
clear = pattern2.sub(r'\g<word>', "반반복복되되는 문자를 지지워워주세요요")  # name 사용
print (clear)

p = re.compile(".*[.][^bat].*$")
m = p.search("autoexec.bat")
print (m)
