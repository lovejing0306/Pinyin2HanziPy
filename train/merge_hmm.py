# coding=utf-8

import sys
import json

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

ORIGINAL_BASE_START = '../data/train/original/base_start.json'
ORIGINAL_BASE_EMISSION = '../data/train/original/base_emission.json'
ORIGINAL_BASE_TRANSITION = '../data/train/original/base_transition.json'

OTHER_BASE_START = '../data/train/result/other_base_start.json'
OTHER_BASE_EMISSION = '../data/train/result/other_base_emission.json'
OTHER_BASE_TRANSITION = '../data/train/result/other_base_transition.json'

BASE_START = '../data/train/result/base_start.json'
BASE_EMISSION = '../data/train/result/base_emission.json'
BASE_TRANSITION = '../data/train/result/base_transition.json'


def writejson2file(obj, filename):
    with open(filename, 'w') as outfile:
        data = json.dumps(obj, indent=4, sort_keys=True)
        outfile.write(data)


def readdatafromfile(filename):
    with open(filename) as outfile:
        return json.load(outfile)


def merge_start():
    start = {}
    original_start=readdatafromfile(ORIGINAL_BASE_START)
    other_start = readdatafromfile(OTHER_BASE_START)
    for hanzi in original_start.keys():
        count=original_start[hanzi]
        if hanzi in other_start.keys():
            count+=other_start[hanzi]
        else:
            pass
        start[hanzi]=count
    for hanzi in other_start.keys():
        if hanzi in start.keys():
            pass
        else:
            start[hanzi]=other_start[hanzi]
    return start


def merge_emission():
    emission={}
    original_emission=readdatafromfile(ORIGINAL_BASE_EMISSION)
    other_start=readdatafromfile(OTHER_BASE_EMISSION)
    for hanzi in original_emission.keys():
        if hanzi in other_start.keys():
            pinyins={}
            for pinyin in original_emission[hanzi].keys():
                count=original_emission[hanzi][pinyin]
                if pinyin in other_start[hanzi].keys():
                    count+=other_start[hanzi][pinyin]
                else:
                    pass
                pinyins[pinyin]=count
            emission[hanzi]=pinyins
        else:
            emission[hanzi]=original_emission[hanzi]
    return emission


def merge_transition():
    transition={}
    original_transition=readdatafromfile(ORIGINAL_BASE_TRANSITION)
    other_transition=readdatafromfile(OTHER_BASE_TRANSITION)

    for hanzi in original_transition.keys():
        if hanzi in other_transition.keys():
            hanzis_trans={}
            for hanzi_trans in original_transition[hanzi].keys():
                count=original_transition[hanzi][hanzi_trans]
                if hanzi_trans in other_transition[hanzi].keys():
                    count+=other_transition[hanzi][hanzi_trans]
                else:
                    pass
                hanzis_trans[hanzi_trans]=count
            transition[hanzi]=hanzis_trans
        else:
            transition[hanzi]=original_transition[hanzi]

    for hanzi in other_transition.keys():
        if hanzi in transition.keys():
            for hanzi_trans in other_transition[hanzi].keys():
                if hanzi_trans in transition[hanzi].keys():
                    pass
                else:
                    transition[hanzi][hanzi_trans]=other_transition[hanzi][hanzi_trans]
        else:
            transition[hanzi]=other_transition[hanzi]
    return transition


def merge_gen_base():
    writejson2file(merge_start(), BASE_START)
    writejson2file(merge_emission(), BASE_EMISSION)
    writejson2file(merge_transition(), BASE_TRANSITION)


def main():
    merge_gen_base()


if __name__ == '__main__':
    main()
