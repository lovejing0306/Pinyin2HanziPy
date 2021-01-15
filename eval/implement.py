# coding: utf-8
import sys
sys.path = ['../..'] + sys.path
from .interface import AbstractHmmParams, AbstractDagParams
from pinyin2hanzi_01.util import as_text
from pinyin2hanzi_01.util import normlize_pinyin
import os
import json


DATA    = 'data'
DEFAULT = 'default'

## HMM模型
class DefaultHmmParams(AbstractHmmParams):

    def __init__(self,):
        current_dir = self.pwd()
        self.py2hz_dict      = self.readjson(os.path.join(current_dir, '../data/train/result', 'hmm_py2hz.json'))  # 一个读音对应多个汉字
        self.start_dict      = self.readjson(os.path.join(current_dir, '../data/train/result', 'hmm_start.json'))
        self.emission_dict   = self.readjson(os.path.join(current_dir, '../data/train/result', 'hmm_emission.json'))
        self.transition_dict = self.readjson(os.path.join(current_dir, '../data/train/result', 'hmm_transition.json'))

    ## 读取json文件
    def readjson(self, filename):
        with open(filename) as outfile:
            return json.load(outfile)

    ## 给出当前文件所在的目录
    def pwd(self):
        return os.path.dirname(os.path.abspath(__file__))

    ## 获取开始概率
    def start(self, state):
        ''' get start prob of state(hanzi)
            state:一个汉字
        '''
        state = as_text(state) # 转换汉字的字符集

        data = self.start_dict[DATA]  # 读取data元素中的数据集
        default = self.start_dict[DEFAULT] # 读取default元素中的数据集

        # 如果汉字state在data表示的字典中，则取出该汉字的概率，否则使用默认的概率
        if state in data:
            prob = data[state]
        else:
            prob = default
        return float(prob)  # 返回汉字state的概率

    ## 获取汉字->拼音的发射概率
    def emission(self, state, observation):
        ''' state (hanzi) -> observation (pinyin) '''
        # 编码
        pinyin = as_text(observation)
        hanzi = as_text(state)

        data = self.emission_dict[DATA]   # 获取准备好的发射概率
        default = self.emission_dict[DEFAULT]    # 获取默认的发射概率

        # 如果汉字不在data中返回默认的发射概率
        if hanzi not in data:
            return float( default )
        
        prob_dict = data[hanzi]

        if pinyin not in prob_dict:
            return float( default )
        else:
            return float( prob_dict[pinyin] )

    ## 计算转移概率
    def transition(self, from_state, to_state):
        ''' state -> state '''
        from_state = as_text(from_state)
        to_state = as_text(to_state)
        prob = 0.0

        data = self.transition_dict[DATA]
        default = self.transition_dict[DEFAULT]

        if from_state not in data:
            return float( default )
        
        prob_dict = data[from_state]

        if to_state in prob_dict:
            return float( prob_dict[to_state] )
        
        if DEFAULT in prob_dict:
            return float( prob_dict[DEFAULT] )

        return float( default )

    ## 获取某个拼音的所有可能的汉字
    def get_states(self, observation):
        ''' get states which produce the given obs '''
        return [hanzi for hanzi in self.py2hz_dict[normlize_pinyin(observation)]] # 获取拼音可能的汉字之前先对拼音进行标准化


## DAG模型
class DefaultDagParams(AbstractDagParams):

    def __init__(self,):
        current_dir = self.pwd()
        self.char_dict      = self.readjson(os.path.join(current_dir, 'data', 'dag_char.json'))
        self.phrase_dict    = self.readjson(os.path.join(current_dir, 'data', 'dag_phrase.json'))

    def readjson(self, filename):
        with open(filename) as outfile:
            return json.load(outfile)

    def pwd(self,):
        return os.path.dirname(os.path.abspath(__file__))

    def get_phrase(self, pinyin_list, num=6):
        ''' pinyin_list是拼音组成的list，例如['yi', 'ge'] '''
        if len(pinyin_list) == 0:
            return []
        if len(pinyin_list) == 1:
            data = self.char_dict
        else:
            data = self.phrase_dict

        pinyin = ','.join(pinyin_list)

        if pinyin not in data:
            return []

        return data[pinyin][:num]
        

