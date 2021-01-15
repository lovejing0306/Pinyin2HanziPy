#coding=utf-8

from ChineseTone import PinyinHelper
import sys
sys.path = ['../../pinyin2hanzi_01'] + sys.path # 将pinyin2hanzi_01导入检索路径
import util

def topinyin(s):
    """
    s都是汉字
    """
    s = util.as_text(s)
    py_list = PinyinHelper.convertToPinyinFromSentence(s)
    result = []
    for py in py_list:
        py = util.as_text(py)
        if py == '〇':
            result.append('ling')
        else:
            result.append(util.simplify_pinyin(py))

    if ',' in ''.join(result):
        print(s)
        print(''.join(result))
        sys.exit()
    return result

def hanzi2pinyin(original_file, trans_file):
    with open(trans_file, 'w') as f_writer:
        with open(original_file, 'r') as f_reader:
            for line in f_reader:
                try:
                    line=line.strip()
                    pinyin='#'.join(topinyin(line))
                    result=line+'\t'+pinyin+'\n'
                    f_writer.write(result)
                except Exception as e:
                    print(e)
                    continue

if __name__=='__main__':
    original_file='../data/pre/original/name_all.txt'
    trans_file='../data/pre/result/name_all_pinyin.txt'
    hanzi2pinyin(original_file, trans_file)