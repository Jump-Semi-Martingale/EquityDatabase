# -*- coding: utf-8 -*-
# python 2.7

import csv

if __name__ == '__main__':
    
    ff = open('CA.txt')
    data1 = ff.read()  # ファイル終端まで全て読んだデータを返す
    data2=data1.split(' ')
    ff.close()
    print len(data2)
    with open('CA2.txt', 'w') as f:
        #writer = csv.writer(f)  # writerオブジェクトを作成
        #writer.writerows(data2)  # 内容を書き込む
        for i in range(0,len(data2)-1,1):
            aa=data2[i]
            f.write(aa)
            f.write('\n')
        f.close