#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 21:40:32 2018

@author: jishuai
"""

import os
import time
    
while True:
    try:
        os.system('python merukari_search.py')
        time.sleep(5)
    except KeyboardInterrupt:
        print('Manual break by user')
        break