# -*- coding: utf-8 -*-
# python 2.7
import lxml.html
from lxml import etree
import datetime
import json
import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
#import requesocks
#import csv



def newIdentity(self):
    socks.setdefaultproxy()
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9051))
    s.send('AUTHENTICATE "Akihiko_1234" \r\n')
    response = s.recv(128)
    if response.startswith("250"):
        s.send("SETCONF ExitNodes={in}\r\n")
        s.send("SETCONF StrictNodes=1\r\n")
        s.send("SIGNAL NEWNYM\r\n")
    s.close()
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def getCODE(date_str):
    #with Controller.from_port(port = 9051) as controller:
    #    controller.authenticate(password='Akihiko_1234')
    #    controller.signal(Signal.NEWNYM)
    
    url = 'http://k-db.com/stocks/{date_str}'
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19')
    html = urllib2.urlopen(req).read()
    tree = lxml.html.fromstring(html)
    contents = map(lambda html: html.text.encode('utf-8'), tree.xpath('//*[@id="maintable"]//td/a'))
    
    res = []
    for i in range(0, len(contents)-1,1):
        sec_code_name=contents[i]
        if sec_code_name[5]=='T':
            sec_code=sec_code_name[0:4]
            res.append(sec_code) #([])ではなく、()にするとCODEが[]でなくなり、t_dateが入る
    return res

def getNAV(fundcode, year):
    #with Controller.from_port(port = 9051) as controller:
    #    controller.authenticate(password='Akihiko_1234')
    #    controller.signal(Signal.NEWNYM)
    
    d = dict(fundcode=fundcode, year=year)
    #newIdentity()

    socks.setdefaultproxy()
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9051))
    s.send('AUTHENTICATE "Akihiko_1234" \r\n')
    response = s.recv(128)
    if response.startswith("250"):
        s.send("SETCONF ExitNodes={in}\r\n")
        s.send("SETCONF StrictNodes=1\r\n")
        s.send("SIGNAL NEWNYM\r\n")
    s.close()
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    
    url = 'http://k-db.com/stocks/{fundcode}-T/1d/{year}'.format(**d)
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19')
    html = urllib2.urlopen(req).read()
    tree = lxml.html.fromstring(html)
    contents = map(lambda html: html.text, tree.xpath('//*[@id="maintable"]//td'))

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
    socks.setdefaultproxy()
    return res


def postDB(post_data):
    response = requests.post('http://54.199.174.85:3000/api/equities', post_data)




if __name__ == '__main__':
    #session = requesocks.session()
    #session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
    #print session.get('http://httpbin.org/ip').text
    
    date_str='2016-06-10'
    import socks
    import socket
    import urllib2
    codelist=getCODE(date_str)
    #print(codelist)
    codelist=codelist[2244:]#79名柄分[0:78]終わっている1950から
    #codelist = codelist[0:1] #とりま1銘柄分
    #print(codelist)
    rows=[]
    for i in range(0, len(codelist),1):
        args = dict(fundcode=codelist[i], year='2016') #fundnameをここに追加したい
        rows = getNAV(**args)
        import socks
        import socket
        import urllib2
        for j in range(0,len(rows),1):
            tmp=rows[j]
            #print(tmp)
            postDB(tmp)


"""
    with open('Test_Codelist.csv', 'w') as f:
    writer = csv.writer(f)  # writerオブジェクトを作成
    writer.writerows(codelist)  # 内容を書き込む
    """