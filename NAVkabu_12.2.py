# -*- coding: utf-8 -*-
# python 2.7
import lxml.html
import datetime
import json
import requests
#import time
#import csv


def getCODE(date_str):
    
    # dictをアンパックしてURL生成
    url = 'http://k-db.com/stocks/{date_str}'
    
    # ElementTreeを取得
    tree = lxml.html.parse(url)
    
    # 日付, 基準価額, 純資産の要素をすべて取得しつつ、mapを適用してutf-8化とカンマ除去
    contents = map(lambda html: html.text.encode('utf-8'), tree.xpath('//*[@id="maintable"]//td/a'))
    #contents = map(lambda html: lxml.html.tostring(html, method='text', encoding='utf-8'), tree.xpath('//*[@id="maintable"]//td/a'))
    #contents2 = map(lambda html: lxml.html.tostring(html, method='text', encoding='cp932'), tree.xpath('//*[@id="maintable"]//td/a'))
    
    #print contents
    # ひとつのリストになっているので[[t_date, price, cap], [t_date, price, cap], ...]と分ける
    res = []
    for i in range(0, len(contents)-1,1):
        sec_code_name=contents[i]
        #test_name=contents2[i]
        #if i<3: print(sec_code_name[7:]) #sec_nameが文字化けしてしまうが、本来的にはここで取り込みたい
        #if i<3: print(test_name[7:])
        if sec_code_name[5]=='T':
            sec_code=sec_code_name[0:4]
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
    # ひとつのリストになっているので[[date, price, cap], [date, price, cap], ...]と分ける
    res = []
    for i in range(0, len(contents)-1, 9):
        t_date = contents[i]   #文字列なのでjson形式にする場合でも問題ない
        start_price = contents[i+2]
        max_price=contents[i+3]
        min_price=contents[i+4]
        end_price=contents[i+5]
        trade_volume=contents[i+6]
        trade_amount=contents[i+7]
        sec_code=fundcode[0:4]
        #追加したいが、文字化け未対応
        #sec_name=fundname???　　　#, 'sec_name':sec_name
        temp=str(sec_code)
        temp2=t_date.replace('-','')
        key_id=temp+temp2
        jsondata = {'key_id':key_id, 't_date':t_date, 'sec_code':sec_code, 'start_price':start_price, 'max_price':max_price, 'min_price':min_price,'end_price':end_price,'trade_volume':trade_volume,'trade_amount':trade_amount}
        res.append(jsondata)
    return res


def postDB(post_data):
    response = requests.post('http://54.199.174.85:3000/api/equities', post_data)
    #レスポンスオブジェクトのjsonメソッドを使うと、
    #JSONデータをPythonの辞書オブジェクトに変換して取得できる
    #pprint.pprint(response.json())

                             
if __name__ == '__main__':
    
    date_str='2016-06-10'
    codelist=getCODE(date_str)
    codelist=codelist[79:]#79名柄分[0:78]終わっている
    #codelist = codelist[0:1] #とりま1銘柄分
    #print(len(codelist))
    #print(codelist)
    
    #rowsDB=[]
    rows=[]
    for i in range(0, len(codelist),1):
        args = dict(fundcode=codelist[i], year='2016') #fundnameをここに追加したい
        rows = getNAV(**args)

        for j in range(0,len(rows),1):
            tmp=rows[j]
            #tmp=rows[0]
            #print(tmp)
            postDB(tmp)

        

"""
        if i == 0:
            rowsDB=rows
        else:
            rowsDB.extend(rows)

    Num = len(rowsDB)
    #print Num

    for j in range(0,Num):
        tmp = rowsDB[j]
        #print tmp
        postDB(tmp)
"""


"""
    #JSON形式で保存
    f = open('TEST.json', 'w')
    json.dump(rowsDB,f)
"""




"""
    #JSON形式で保存
    f = open('Sec_Code_List.json', 'w')
    json_data = {'t_date', 'fundcode', 'start_price', 'max_price','min_price','end_price','trade_volume','trade_amount':(rowsDB)}
    json.dump(json_data,f)
"""


