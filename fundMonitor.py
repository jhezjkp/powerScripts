#!/usr/bin/env python
#encoding=utf-8

'''
基金风险监控脚本
需要requests和BeautifulSoup支持
'''

import sys
import os
import os.path
import urllib
import requests
from BeautifulSoup import BeautifulSoup


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    pageUrl = "http://fund.eastmoney.com/000198.html"
    r = requests.get(pageUrl)
    if r.status_code == 200:
    	print unicode(r.text)
        soup = BeautifulSoup(r.text, fromEncoding="gb18030")
        print soup.originalEncoding
        fundTable = soup.find("table", {"class": "sytable"}).findAll("td")
        print unicode(fundTable[0].text)
        print fundTable[0].text

