#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

import pandas as pd
import numpy as np

cuts_filepath = r'data/travel/results_cuts_all.csv'
content = pd.read_csv(cuts_filepath,encoding='gbk')
print(content.head(5))