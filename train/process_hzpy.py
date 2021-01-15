# coding: utf-8

from __future__ import (print_function, unicode_literals)

import os
import sys
sys.path = ['../../pinyin2hanzi_01'] + sys.path # 将pinyin2hanzi_01导入检索路径
import util

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

SOURCE_FILE           = '../data/train/original/hanzipinyin.txt'

ALL_STATES_FILE       = '../data/train/result/all_states.txt'         # 汉字（隐藏状态）
ALL_OBSERVATIONS_FILE = '../data/train/result/all_observations.txt'   # 拼音（观测值）
PINYIN2HANZI_FILE     = '../data/train/result/pinyin2hanzi.txt'

states = set()
observations = set()
py2hz = {}


for line in open(SOURCE_FILE):
    line = util.as_text(line.strip())
    hanzi, pinyin_list = line.split('=')
    pinyin_list = [util.simplify_pinyin(item.strip()) for item in pinyin_list.split(',')]

    states.add(hanzi)
    
    for pinyin in pinyin_list:
        observations.add(pinyin)
        py2hz.setdefault(pinyin, set())
        py2hz[pinyin].add(hanzi)
        # 声母
        shengmu = util.get_shengmu(pinyin)
        if shengmu is not None:
            py2hz.setdefault(shengmu, set())
            py2hz[shengmu].add(hanzi) 

with open(ALL_STATES_FILE, 'w') as out:
    s = '\n'.join(states)
    out.write(s)

with open(ALL_OBSERVATIONS_FILE, 'w') as out:
    s = '\n'.join(observations)
    out.write(s)

with open(PINYIN2HANZI_FILE, 'w') as out:
    s = ''
    for k in py2hz:
        s = s + k + '=' + ''.join(py2hz[k]) + '\n'
    out.write(s)

print('end')