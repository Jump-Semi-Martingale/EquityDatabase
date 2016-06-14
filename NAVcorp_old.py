# -*- coding: utf-8 -*-
# python 2.7
import lxml.html
import datetime
import json
import requests


def getCA():
    url = 'http://minkabu.jp/top/stock_news'
    tree = lxml.html.parse(url)
    contents = map(lambda html: html.text, tree.xpath('//*[@id="ajax_update_stock_news"]//td'))
    contents2=map(lambda html: html.text, tree.xpath('//*[@id="ajax_update_stock_news"]//td/a'))
    for i in range(0,len(contents)-1,1):
        if contents[i]==None:
            contents[i]=0
        else:
            contents[i]=contents[i].encode('utf-8')
    j=0
    res=[]
    for i in range(2,len(contents)-1,5):
        if contents[i+4]==0:
            j=j+1
        else:
            update_date=contents[i]
            corp_date=contents[i+2]
            hold=contents[i+4].split(':')
            corp_rate=float(hold[0])/float(hold[1])
            corp_name=contents2[j].encode('utf-8')
            j=j+1
            jsondata={'update_date':update_date, 'corp_date':corp_date, 'corp_rate':corp_rate, 'corp_name':corp_name}
            res.append(jsondata)

    print(res)
    return res


def postDB(post_data):
    response = requests.post('http://54.199.174.85:3000/api/ca', post_data)

                             
if __name__ == '__main__':
    res=getCA()
    for i in range(0,len(rows),1):
        tmp=res[i]
        postDB(tmp)

