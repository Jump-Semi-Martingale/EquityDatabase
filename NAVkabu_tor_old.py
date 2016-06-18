# -*- coding: utf-8 -*-
# python 2.7
import lxml.html
from lxml import etree
import datetime
import json
import requests
#import time
#import csv
from bs4 import BeautifulSoup
import urllib2
from stem import Signal
from stem.control import Controller
import requesocks


def getCODE(date_str):
    
    url = 'http://k-db.com/stocks/{date_str}'
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19')
    html = urllib2.urlopen(req).read()
    tree = lxml.html.fromstring(html)
    
    #tree = lxml.html.parse(url)
    
    # 日付, 基準価額, 純資産の要素をすべて取得しつつ、mapを適用してutf-8化とカンマ除去
    contents = map(lambda html: html.text.encode('utf-8'), tree.xpath('//*[@id="maintable"]//td/a'))
    
    res = []
    for i in range(0, len(contents)-1,1):
        sec_code_name=contents[i]
        if sec_code_name[5]=='T':
            sec_code=sec_code_name[0:4]
            res.append(sec_code) #([])ではなく、()にするとCODEが[]でなくなり、t_dateが入る
    return res

def getNAV(fundcode, year):
    
    # 引数をdictに突っ込む
    d = dict(fundcode=fundcode, year=year)
    
    # dictをアンパックしてURL生成
    url = 'http://k-db.com/stocks/{fundcode}-T/1d/{year}'.format(**d)
    
    
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19')
    html = urllib2.urlopen(req).read()
    tree = lxml.html.fromstring(html)
    # ElementTreeを取得
    #tree = lxml.html.parse(url)
    
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
    session = requesocks.session()
    session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
    print session.get("http://httpbin.org/ip").text
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password='Akihiko_1234')
        print('Success!')
        controller.signal(Signal.NEWNYM)
        print('New Tor connection processed')
        print session.get("http://httpbin.org/ip").text
    date_str='2016-06-10'
    #codelist=getCODE(date_str)
    #print(codelist)
    
    
    #codelist=codelist[79:]#79名柄分[0:78]終わっている
    
"""
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


"""
    
    with Controller.from_port(port = 9051) as controller:
    controller.authenticate('Akihiko_1234')  # provide the password here if you set one
    bytes_read = controller.get_info('traffic/read')
    bytes_written = controller.get_info('traffic/written')
    
    print('My Tor relay has read %s bytes and written %s.' % (bytes_read, bytes_written))
    """
"""
    #torが機能してるかテスト
    
    #torが機能してるかテストkokomade
"""


