#coding=utf-8


def convert_data_format(original_file, trans_file):
    '''将csv格式的地址数据进行清洗并转换格式
    Args:
        original_file(str):目标文件
        trans_file(str):转换后存放的文件
    Return:
        无
    '''
    with open(trans_file, 'w') as f_writer:
        with open(original_file, 'r') as f_read:
            for line in f_read:
                try:
                    line = line.strip();
                    items = line.split(',')
                    for i in range(0, 5):
                        f_writer.write(items[i] + '\n')
                except Exception as e:
                    print(e)
                    continue


if __name__=='__main__':
    original_file='../data/pre/original/address.csv'
    trans_file='../data/pre/result/address.txt'
    convert_data_format(original_file, trans_file)