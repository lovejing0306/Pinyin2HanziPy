#coding=utf-8

import sys
sys.path = ['../..'] + sys.path
from pinyin2hanzi_01.eval.implement import DefaultHmmParams
from pinyin2hanzi_01.eval.viterbi import viterbi
from pinyin2hanzi_01 import util
# from Pinyin2Hanzi import DefaultHmmParams
# from Pinyin2Hanzi import viterbi

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

if __name__ == '__main__':
    hmmparams = DefaultHmmParams()

    #pinyin=['ni', 'zhi', 'bu', 'zhi', 'dao']
    # pinyin='tiao#yue'
    # result = viterbi(hmm_params=hmmparams, observations=pinyin.split('#'), path_num=2)
    # for item in result:
    #     print(''.join(item.path)+'\t'+str(item.score))

    data_dir = '../data/test/original/test_data.txt'
    dst_fpath = '../data/test/result/pinyin2hanzi_hmm.txt'

    with open(dst_fpath, 'w') as f_write:
        with open(data_dir, 'r') as f_read:
            for line in f_read:
                line = line.strip('\n')
                items = line.split('\t')
                hanzi = items[0]
                pinyin = items[1]
                try:
                    ## 2个候选
                    result = viterbi(hmm_params=hmmparams, observations=[util.normlize_pinyin(item) for item in pinyin.split('#')], path_num=2)

                    for item in result:
                        line=line+'\t'+''.join(item.path)+'\t'+str(item.score)
                        #print()
                except Exception as e:
                    print(e)
                finally:
                    f_write.write(line+'\n')
