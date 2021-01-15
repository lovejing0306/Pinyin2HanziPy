# coding=utf-8

import os
import sys
from xml.dom import minidom

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


## 解析搜狗新闻预料数据集

def file_fill(original_file, trans_file):  # 得到文本.txt的路径
    '''给搜狗语料集加上<docs>-></docs>标签对
    Args:
        original_file(string): 要处理的文本路径
        text_file(String): 清洗完成之后存放的位置
    Return:
        无
    '''
    title = '<?xml version="1.0" encoding="UTF-8"?>\n'
    start = '<docs>\n'
    end = '</docs>\n'

    with open(trans_file, 'w') as f_write:
        f_write.write(title)
        f_write.write(start)
        with open(original_file, 'r') as f_read:
            for line in f_read:
                line = line.replace('&', '')
                f_write.write(line)
        f_write.write(end)


def get_title_content(trans_file, text_file):
    '''获取搜狗新闻语料中title和content
    Args:
        trans_file(string): 要处理的文件的路径
        text_file(string): 存放的位置
    Return:
        无
    '''
    doc = minidom.parse(trans_file)
    root = doc.documentElement
    title = root.getElementsByTagName('contenttitle')
    content = root.getElementsByTagName('content')
    with open(text_file, 'w') as f_write:
        for t, c in zip(title, content):
            try:
                f_write.write(t.firstChild.data + '\n')
            except Exception as e:
                print(e)
            try:
                f_write.write(c.firstChild.data + '\n')
            except Exception as e:
                print(e)


def rename_file(direc_path):
    '''批量重命名文件名
    Args:
        direc_path(String):目录的路径
    Return:
        无
    '''
    i=0
    for file in os.listdir(direc_path):
        if os.path.isfile(os.path.join(direc_path, file)) == True:
            newname = str(i)+".txt"
            os.rename(os.path.join(direc_path, file), os.path.join(direc_path, newname))
            i+=1
        else:
            pass
    print("done!")

def get_text(direc_path, trans_file):
    '''批量读取文件中的文本内容
    Args:
        direc_path(String):目录的路径
    Return:
        无
    '''
    all_files = []
    for root, directories, filenames in os.walk(direc_path):
        for filename in filenames:
            p = os.path.join(direc_path, filename)
            if p.endswith('.txt'):
                all_files.append(p)
    with open(trans_file, 'w') as f_writer:
        for fp in all_files:
            print('process ' + fp)
            with open(fp, 'r') as f_reader:
                for line in f_reader:
                    line=line.strip()
                    items=line.split('\t')
                    f_writer.write(items[0]+'\n')



if __name__ == '__main__':
    # original_file = '../data/original/news_sohusite_xml.utf8'
    # trans_file = '../data/result/trans_corpus.xml'
    # text_file = '../data/result/text_corpus.txt'
    # file_fill(original_file, trans_file)
    # get_title_content(trans_file, text_file)

    direc_path='../data/pre/original/'
    #rename_file(direc_path)
    trans_file='../data/pre/result/other_text_corpus.txt'
    get_text(direc_path, trans_file)