# 拼音转汉字
这是一个训练拼音转汉字的开源项目，基于隐马尔可夫方法。
## 依赖环境
* python3
* ChineseTone

## 项目结构
```
|--data
    |--train
        |--article：存放训练的中文语料
        |--original：一些原始的数据（建议不需要改变）
        |--result：模型训练的结果（以下几个文件比较重要，其它都是一些中间结果）
            |--other_base_start.json：模型合并前用自己的数据训练出来的起始频数文件
            |--other_base_emission.json：模型合并前用自己的数据训练出来的发射频数文件
            |--other_base_transition.json：模型合并前用自己的数据训练出来的转移频数文件
            |--base_start.json：合并后的起始频数文件
            |--base_emission.json：合并后的发射频数文件
            |--base_transition.json：合并后的转移频数文件
            |--hmm_start.json：合并后的起始概率文件
            |--hmm_emission.json：合并后的发射概率文件
            |--hmm_transition.json：合并后的的转移概率文件
            |--hmm_py2hz.json：拼音汉字对照文件
            |--original_hmm_start.json：原始的起始概率文件
            |--original_hmm_emission.json：原始的发射概率文件
            |--original_hmm_transition.json：原始的转移概率文件
            |--original_hmm_py2hz.json：原始的拼音汉字对照文件
|--train
    |--process_article.py：处理输入的中文文本语料
    |--gen_base.py：生成 other_base_start.json、other_base_emission.json和other_base_transition.json 文件
    |--merge.py：将 other_base_*.json 文件与原始的 base_*.json 文件合并
    |--process_finally.py：生成HMM模型（hmm_*.json）
```

## 预训练模型及其他文件
|网盘    |链接    |
| :---: |:---:  |
|baidu| [下载 e7k6](https://pan.baidu.com/s/1e7G68DVyflj8UxpFBHrPxg)|
|google| [下载](https://drive.google.com/drive/folders/1jaay7dKEiOEuIfLoDmj6YLxbECDzhiMW?usp=sharing)|

> 将下载的数据放到 data 目录下。

## 训练
训练分两种情况：
* 不与原始模型合并
* 与原始（现有）的模型合并

### 不与原始模型合并
依次执行以下py脚本：
```
python3 process_article.py
python3 gen_base.py(注意：在此步完成之后需要将other_base_*.json文件重命名为base_*.json)
python3 process_finally.py
```

### 与原始（现有）的模型合并
依次执行以下py脚本：
```
python3 process_article.py 
python3 gen_base.py 
python3 merge_hmm.py 
python3 process_finally.py
```
> 适用于你所拥有的中文训练语料较少的情况

## 使用
跳转项目至 [pinyin2hanzi Java](https://github.com/lovejing0306/pinyin2hanzi)