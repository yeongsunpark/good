#!/usr/bin/env python
 
import os
day = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21","22","23","24","25","26","27","28","29","30", "31"]
# day = ["01", "03", "05", "07", "09", "11", "13", "15", "17", "19", "21", "23", "25", "27", "29","31"]
# day = ["31"]
#for i in day[:31]:
for i in day:
    os.system('python ys_xml.py ~/maum/resources/MRC/4100058_nocut/2018/12/{}'.format(i))
    print ('python ys_xml.py ~/maum/resources/MRC/4100058_nocut/02/{}'.format(i))