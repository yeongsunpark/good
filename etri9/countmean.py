#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-06-03

import pandas as pd
import numpy as np
import json

df = pd.read_csv("/home/msl/ys/cute/data/cw0530/result_morp/stati.txt", error_bad_lines=False, sep='\t', header = None)
a = df[1]
print (np.mean(a))