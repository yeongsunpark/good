#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-15

import math
import random

contexts = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h", 9:"i", 10:"j"}
a_cnt = math.floor((len(contexts)) * 0.7)
a = random.sample(contexts, a_cnt)
print (len(a))

b_tmp = [c for c in contexts if c not in a]

b_cnt = math.floor((len(contexts)-len(a)) * 0.5)
b = random.sample(b_tmp, b_cnt)
print (len(b))

c_tmp = [c for c in contexts if c not in a and c not in b]

print (len(c_tmp))