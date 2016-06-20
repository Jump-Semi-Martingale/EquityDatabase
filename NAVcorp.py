# -*- coding: utf-8 -*-
# python 2.7
import lxml.html
import datetime
import json
import requests
import re

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
            update_date=contents[i].replace('/','-')
            corp_date=contents[i+2].replace('/','-')
            hold=contents[i+4].split(':')
            corp_rate=float(hold[1])/float(hold[0])
            corp_name=contents2[j].encode('utf-8')
            corp_name=re.findall('\([0-9]+[0-9]+[0-9]+[0-9]+\)', corp_name)
            corp_name=re.findall('[0-9]+[0-9]+[0-9]+[0-9]+', corp_name[0])
            corp_name=corp_name[0]
            temp=str(corp_name)
            temp2=corp_date.replace('-','')
            key_id=temp+temp2
            j=j+1
            jsondata={'update_date':update_date, 'corp_date':corp_date, 'corp_rate':corp_rate, 'corp_name':corp_name,'key_id':key_id}
            res.append(jsondata)

    print(res)
    return res


def postDB(post_data):
    response = requests.post('http://54.199.174.85:3000/api/cas', post_data)

                             
if __name__ == '__main__':
    rows=getCA()
    for i in range(0,len(rows),1):
        tmp=rows[i]
        postDB(tmp)