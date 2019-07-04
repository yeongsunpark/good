#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-02

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.font_manager as fm

with open("/home/msl/ys/cute/data/news/대화로그분류.txt", encoding="utf-8-sig") as f:
    data= f.readlines()
    count_dict = dict()
    for d in data:
        d = d.strip()
        if d in count_dict:
            count_dict[d] +=1
        else:
            count_dict[d] = 1
print (count_dict)

# path = '/usr/share/fonts/nhn-nanum/NanumGothicExtraBold.ttf'
# fontprop = fm.FontProperties(fname=path, size=18)
# font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
# print (font_list[:10])
# print ([(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name])
font_location = '/usr/share/fonts/nhn-nanum/NanumGothicExtraBold.ttf'
font_name = fm.FontProperties(fname = font_location).get_name()
matplotlib.rc('font', family = font_name)

y = count_dict.values()
x = np.arange(len(y))
xlabel = count_dict.keys()
plt.title("Bar Chart")
plt.bar(x, y)
plt.xticks(x, xlabel)
plt.yticks(sorted(y))
plt.xlabel("카테고리")
plt.ylabel("빈도수")
plt.savefig ("/home/msl/ys/cute/data/news/test_figure1.png",dpi=300)