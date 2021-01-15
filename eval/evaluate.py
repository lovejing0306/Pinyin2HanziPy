#coding=utf-8

import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

## 计算目标汉字和生成汉字之间的相似度
def cal(l1, l2):
    """添加转移记录
    Args:
        l1 (list): 目标汉字列表
        l2(string): 生成汉字列表
    Return：
        汉字之间的相似度
    """
    if l1 is None or l2 is None:
        return 0.0
    count=0
    if len(l1) >= len(l2):
        for i in range(0, len(l2)):
            if l1[i]==l2[i]:
                count+=1
    else:
        for i in range(0, len(l1)):
            if l1[i]==l2[i]:
                count+=1
    return (count+0.000000002)/(len(l1)+0.000000001)

## 将汉字字符串转换成汉字列表
def str2list(str):
    #str=str.decode('utf-8')
    l=[]
    for i in str:
        l.append(i)
    return l

## 获取生成的汉字字符串列表
def get_hanzis(items):
    size=len(items)
    n=int((size-2)/2)
    l=[]
    for i in range(n+1):
        l.append(items[i*2])
    return l

## 评估HMM模型
def eval(dst_fpath, dst_error, rate_threshold):
    count = 0
    ecpt_num = 0
    line_num = 0
    with open(dst_error, 'w') as f_write:
        with open(dst_fpath, 'r') as f_read:
            for line in f_read:
                line_num = line_num + 1
                line = line.strip('\n')
                items = line.split('\t')
                try:
                    hanzis = get_hanzis(items)
                    hanzis_list = []
                    for hanzi in hanzis:
                        hanzis_list.append(str2list(hanzi))

                    rates = []
                    for i in range(1, len(hanzis_list)):
                        rates.append(cal(hanzis_list[0], hanzis_list[i]))

                    rate = max(rates)
                    if rate >= rate_threshold:
                        count = count + 1
                    else:
                        f_write.write(line + '\n')
                except Exception as e:
                    f_write.write(line + '\n')
                    print(e)
                    ecpt_num = ecpt_num + 1

    eval_result = count / (line_num + 0.0000000001)
    print('异常数据：' + str(ecpt_num))
    print('测试总数：' + str(line_num))
    print('匹配数量：' + str(count))
    print('命中率：' + str(eval_result))


if __name__=='__main__':
    dst_fpath = '../data/test/original/name_all_pinyin_pinyin2hanzi_03.txt'
    dst_error = '../data/test/result/name_all_pinyin_pinyin2hanzi_error_03.txt'
    rate_threshold=0.5
    eval(dst_fpath, dst_error, rate_threshold)

    str1='不当得利'
    str2='不当得利'
    l1=str2list(str1)
    l2=str2list(str2)
    print(cal(l1, l2))