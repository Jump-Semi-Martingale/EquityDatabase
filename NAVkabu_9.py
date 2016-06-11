# -*- coding: utf-8 -*-
# python 2.7
import lxml.html
import datetime
import json
import requests
#import csv


def getCODE(date_str):
    
    # dictをアンパックしてURL生成
    url = 'http://k-db.com/stocks/{date_str}'
    
    # ElementTreeを取得
    tree = lxml.html.parse(url)
    
    # 日付, 基準価額, 純資産の要素をすべて取得しつつ、mapを適用してutf-8化とカンマ除去
    contents = map(lambda html: html.text.encode('utf-8'), tree.xpath('//*[@id="maintable"]//td/a'))
    #print contents
    # ひとつのリストになっているので[[t_date, price, cap], [t_date, price, cap], ...]と分ける
    res = []
    for i in range(0, len(contents)-1,1):
        sec_code = contents[i]
        #jojo_place=contents[i+1]
        #start_price = contents[i+2]
        #max_price=contents[i+3]
        #min_price=contents[i+4]
        #end_price=contents[i+5]
        #trade_volume=contents[i+6]
        #trade_amount=contents[i+7]
        #res.append([sec_code,jojo_place, start_price, max_price,min_price,end_price,trade_volume,trade_amount])
        sec_code=sec_code[0:4]
        res.append(sec_code) #([])ではなく、()にするとCODEが[]でなくなり、t_dateが入る
    return res

def getNAV(fundcode, year):
    # 引数をdictに突っ込む
    
    d = dict(fundcode=fundcode, year=year)
    
    # dictをアンパックしてURL生成
    url = 'http://k-db.com/stocks/{fundcode}-T/1d/{year}'.format(**d)
    
    # ElementTreeを取得
    tree = lxml.html.parse(url)
    
    # 要素全て取得
    contents = map(lambda html: html.text, tree.xpath('//*[@id="maintable"]//td'))
    #print contents
    # ひとつのリストになっているので[[t_date, price, cap], [t_date, price, cap], ...]と分ける
    res = []
    for i in range(0, len(contents)-1, 9):
        t_date = contents[i] #文字列なのでjson形式でもOK
        start_price = contents[i+2]
        max_price=contents[i+3]
        min_price=contents[i+4]
        end_price=contents[i+5]
        trade_volume=contents[i+6]
        trade_amount=contents[i+7]
        sec_code=fundcode[0:4]
        temp=str(sec_code)
        key_id=temp+'_'+t_date
        jsondata = {'key_id':key_id, 't_date':t_date, 'sec_code':sec_code, 'start_price':start_price, 'max_price':max_price, 'min_price':min_price,'end_price':end_price,'trade_volume':trade_volume,'trade_amount':trade_amount}
        res.append(jsondata)
    return res

def main(post_data):
    response = requests.post('http://54.199.174.85:3000/api/equities', json, post_data)
    #レスポンスオブジェクトのjsonメソッドを使うと、
    #JSONデータをPythonの辞書オブジェクトに変換して取得できる
    pprint.pprint(response.json())

                             
if __name__ == '__main__':
    
    date_str='2016-06-01'
    codelist = getCODE(date_str)
    codelist = codelist[1:3]#とりま２行分
    
    #print len(codelist)
    #print codelist[0],codelist[1]
    # dictにcodelistを順に突っ込む
    
    rowsDB=[]
    for i in range(0, len(codelist),1):
        args = dict(fundcode=codelist[i], year='2016')
        rows = getNAV(**args)

        if i == 0:
            rowsDB=rows
        else:
            rowsDB.extend(rows)

    main(rowsDB)



"""
    #JSON形式で保存
    f = open('TEST.json', 'w')
    json.dump(rowsDB,f)
"""




"""
    ##############################################
    #JSON形式で保存
    f = open('Sec_Code_List.json', 'w')
    json_data = {'t_date', 'fundcode', 'start_price', 'max_price','min_price','end_price','trade_volume','trade_amount':(rowsDB)}
    json.dump(json_data,f)
"""

"""
    ##############################################
    # ヘッダー
    head=['sec_code']
    #ファイルを書き込みモードでオープン
    with open('2016-06-01.csv', 'w') as f:
        writer = csv.writer(f)  # writerオブジェクトを作成
        writer.writerow(head) # ヘッダーを書き込む
        writer.writerows(codelist)  # 内容を書き込む

    # ヘッダー
    head = ['t_date', 'fundcode', 'start_price', 'max_price','min_price','end_price','trade_volume','trade_amount']
    #ファイルを書き込みモードでオープン
    with open('Test_Codelist.csv', 'w') as f:
        writer = csv.writer(f)  # writerオブジェクトを作成
        writer.writerow(head) # ヘッダーを書き込む
        writer.writerows(rowsDB)  # 内容を書き込む
    #以下、日付指定版
"""


