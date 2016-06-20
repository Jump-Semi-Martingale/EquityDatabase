# -*- coding: utf-8 -*-
# python 2.7
import json
import requests
import csv

if __name__ == '__main__':
    
    f = open('CAs.csv', 'rb')
    dataReader = csv.reader(f)
    first_check=0
    for row in dataReader:
        if first_check==0:
            first_check=1
        else:
            jsondata={'update_date':row[0], 'corp_date':row[1], 'corp_rate':row[3], 'corp_name':row[2],'key_id':row[4]}
            #print jsondata
            response = requests.post('http://54.199.174.85:3000/api/cas', jsondata)
