# coding: utf-8

from __future__ import (print_function, unicode_literals)

import sys
import json
import math

sys.path = ['../../pinyin2hanzi_01'] + sys.path # 将pinyin2hanzi_01导入检索路径
import util


try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

BASE_START_FILE      = '../data/train/result/base_start.json'
BASE_EMISSION_FILE   = '../data/train/result/base_emission.json'
BASE_TRANSITION_FILE = '../data/train/result/base_transition.json'

ALL_STATES_FILE       = '../data/train/result/all_states.txt'   # 所有的字
ALL_OBSERVATIONS_FILE = '../data/train/result/all_observations.txt' # 所有的拼音
PY2HZ_FILE            = '../data/train/result/pinyin2hanzi.txt'

HZ2PY_FILE            = '../data/train/original/hanzipinyin.txt'

FIN_PY2HZ_FILE      = '../data/train/result/hmm_py2hz.json'
FIN_START_FILE      = '../data/train/result/hmm_start.json'
FIN_EMISSION_FILE   = '../data/train/result/hmm_emission.json'
FIN_TRANSITION_FILE = '../data/train/result/hmm_transition.json'


PINYIN_NUM = 411.
HANZI_NUM  = 20903.

def writejson2file(obj, filename):
    with open(filename, 'w') as outfile:
        data = json.dumps(obj, indent=4, sort_keys=True)
        outfile.write(data)

def readdatafromfile(filename):
    with open(filename) as outfile:
        return json.load(outfile)

def gen_py2hz():
    data = {}
    for line in open(PY2HZ_FILE):
        line = util.as_text(line.strip())
        ls = line.split('=')
        if len(ls) != 2:
            raise Exception('invalid format')
        py, chars = ls
        py = py.strip()
        chars = chars.strip()
        if len(py)>0 and len(chars)>0:
            data[py] = chars

    writejson2file(data, FIN_PY2HZ_FILE)

def gen_start():
    data = {'default': 1, 'data': None}
    start = readdatafromfile(BASE_START_FILE)
    count = HANZI_NUM
    for hanzi in start:
        count += start[hanzi]

    for hanzi in start:
        start[hanzi] = round(math.log(start[hanzi] / count), 6)

    data['default'] = round(math.log(1.0 / count), 6)
    data['data'] = start

    writejson2file(data, FIN_START_FILE)

def gen_emission():
    """
    base_emission   = {} #>   {'泥': {'ni':1.0}, '了':{'liao':0.5, 'le':0.5}}
    """
    data = {'default': 1.e-200, 'data': None}
    emission = readdatafromfile(BASE_EMISSION_FILE)


    for line in open(HZ2PY_FILE):
        line = util.as_text(line.strip())
        hanzi, pinyin_list = line.split('=')
        pinyin_list = [util.simplify_pinyin(item.strip()) for item in pinyin_list.split(',')]

        char_list = [hanzi] * len(pinyin_list)
        for hanzi, pinyin in zip(char_list, pinyin_list):
            emission.setdefault(hanzi, {})
            emission[hanzi].setdefault(pinyin, 0.)
            emission[hanzi][pinyin] += 1.

    for hanzi in emission:
        num_sum = 0.
        for pinyin in emission[hanzi]:
            num_sum += emission[hanzi][pinyin]
        for pinyin in emission[hanzi]:
            emission[hanzi][pinyin] = round(math.log(emission[hanzi][pinyin] / num_sum), 6)
    data['default'] = round(math.log(1.e-200), 6)
    data['data'] = emission
    writejson2file(data, FIN_EMISSION_FILE)

def gen_tramsition():
    """  
    {'你': {'好':10, '们':2}, '我': {}}
    """
    data = {'default': 1./HANZI_NUM, 'data': None}
    transition = readdatafromfile(BASE_TRANSITION_FILE)
    for c1 in transition:
        num_sum = HANZI_NUM # 默认每个字都有机会
        for c2 in transition[c1]:
            num_sum += transition[c1][c2]

        for c2 in transition[c1]:
            transition[c1][c2] = round(math.log(float(transition[c1][c2]+1) / num_sum), 6)
        transition[c1]['default'] = round(math.log(1./num_sum), 6)
    data['default'] = round(math.log(1./HANZI_NUM), 6)
    data['data'] = transition
    writejson2file(data, FIN_TRANSITION_FILE)


def main():
    gen_py2hz()
    gen_start()
    gen_emission()
    gen_tramsition()


if __name__ == '__main__':
    main()