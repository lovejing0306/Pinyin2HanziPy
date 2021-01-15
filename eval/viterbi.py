# coding: utf-8
from .interface import AbstractHmmParams
from .priorityset import PrioritySet
import math

def viterbi(hmm_params, observations, path_num=6, log=False, min_prob=3.14e-200):
    '''
    :param hmm_params: hmm用到的参数
    :param observations: 要转换的拼音
    :param path_num: 候选结果的数量
    :param log: 是否按照log的方式计算分数
    :param min_prob: 定义一个最小概率作为阈值
    :return:返回每个候选结果和其对应的分数
    '''

    # 判断hmm_params是否是AbstractHmmParams的一个实体
    assert( isinstance(hmm_params, AbstractHmmParams) )

    V = [{}]

    # 获取观测序列的第一个拼音
    t = 0
    cur_obs = observations[t]
    
    # Initialize base cases (t == 0)
    # 获取第一个拼音的所有可能的汉字
    prev_states = cur_states = hmm_params.get_states(cur_obs)  # wordset
    # 遍历第一个拼音的所有可能的汉字
    for state in cur_states:
        if log:
            __score   = math.log(max(hmm_params.start(state), min_prob)) + \
                math.log(max(hmm_params.emission(state, cur_obs), min_prob))
        else: # 汉字的概率*汉字->拼音的概率
            __score   = max(hmm_params.start(state), min_prob) * \
                max(hmm_params.emission(state, cur_obs), min_prob)
        __path    = [state]
        V[0].setdefault(state, PrioritySet(path_num))   # V[0]是一个字典，setdefault相当于给字典加值，key=state:value=PrioritySet(path_num)
        V[0][state].put(__score, __path)

    
    # Run Viterbi for t > 0
    # 遍历剩余的拼音
    for t in range(1, len(observations)):
        cur_obs = observations[t]

        if len(V) == 2:
            V = [V[-1]]

        V.append({})

        prev_states = cur_states  # 把之前拼音对应的汉字集变成pre_states
        cur_states = hmm_params.get_states(cur_obs)  # 获取当前拼音的汉字集

        for y in cur_states:
            V[1].setdefault( y, PrioritySet(path_num) )
            max_item = None
            for y0 in prev_states:  # from y0(t-1) to y(t)
                for item in V[0][y0]:
                    if log:
                        _s = item.score + \
                            math.log(max(hmm_params.transition(y0, y), min_prob)) + \
                            math.log(max(hmm_params.emission(y, cur_obs), min_prob))
                    else:
                        _s = item.score * \
                            max(hmm_params.transition(y0, y), min_prob) * \
                            max(hmm_params.emission(y, cur_obs), min_prob)

                    _p = item.path + [y]
                    V[1][y].put(_s, _p)

    result = PrioritySet(path_num)
    for last_state in V[-1]:
        for item in V[-1][last_state]:
            result.put(item.score, item.path)
    result = [item for item in result]

    return sorted(result, key=lambda item: item.score, reverse=True)