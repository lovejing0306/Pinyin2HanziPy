#coding=utf-8

import sys
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

if __name__ == '__main__':

    data_dir = './original_corpus.txt'
    dst_fpath = './pinyin2hanzi_dag.txt'

    dagparams = DefaultDagParams()

    with open(dst_fpath, 'w') as f_write:
        with open(data_dir, 'r') as f_read:
            for line in f_read:
                line = line.strip('\n')
                items = line.split('\t')
                hanzi = items[0]
                pinyin = items[1]
                try:
                    ## 2个候选
                    result = dag(dagparams, pinyin.split('#'), path_num=2)
                    for item in result:
                        line = line + '\t' + ''.join(item.path) + ':' + str(item.score)
                except Exception as e:
                    print(e)
                finally:
                    f_write.write(line + '\n')
