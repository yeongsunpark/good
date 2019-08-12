#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-08-08

import pandas as pd
import numpy as np

df = pd.read_csv('grades.csv')
print(len(df))
# 2315

early = df[df['assignment1_submission'] <= '2015-12-31']
late = df[df['assignment1_submission'] > '2015-12-31']

print(early.mean())
'''
assignment1_grade    74.972741
assignment2_grade    67.252190
assignment3_grade    61.129050
assignment4_grade    54.157620
assignment5_grade    48.634643
assignment6_grade    43.838980
dtype: float64
'''

print(late.mean())
'''
assignment1_grade    74.017429
assignment2_grade    66.370822
assignment3_grade    60.023244
assignment4_grade    54.058138
assignment5_grade    48.599402
assignment6_grade    43.844384
dtype: float64
'''

from scipy import stats

t_test1 = stats.ttest_ind(early['assignment1_grade'], late['assignment1_grade'])
print(t_test1)
# Ttest_indResult(statistic=1.400549944897566, pvalue=0.16148283016060577)
# 만일 유의수준 5% (0.05) 로 가설검정을 진행하였을 경우 p-value는 유의수준 a값보다 크므로
# 대립가설은 기각된다.