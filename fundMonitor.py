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
import re
import requests
from BeautifulSoup import BeautifulSoup

#通知邮件地址
email = "fund@vivia.me.mailgun.org"

def send_simple_message(content):
    result = requests.post(
        "https://api.mailgun.net/v2/vivia.me.mailgun.org/messages",
        auth=("api", "key-9lo3lwpmkddrw32r55pcw2dh49prpn00"),
        data={"from": "基金风险监控 <postmaster@vivia.me.mailgun.org>",
              "to": [email],
              "subject": "基金风险报告",
              "text": content})
    print "mail sent!"
    return result

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    pageUrl = "http://fund.eastmoney.com/000198.html"
    r = requests.get(pageUrl)
    if r.status_code == 200:
    	#指定解析编码
    	r.encoding = "gb18030"
        soup = BeautifulSoup(r.text)
        fundTable = soup.find("table", {"class": "sytable"}).findAll("td")
        #万份收益率
        _10kProfit = fundTable[3].text
        _10kProfit = float(_10kProfit[0:_10kProfit.find("&nbsp;")])
        #七日年化收益
        _7DayYearlyProfit = float(fundTable[7].text.replace("%", ""))
        #基金经理
        fundManager = fundTable[19].text.replace("&nbsp;", "").strip()
        print _10kProfit, _7DayYearlyProfit, fundManager
        if fundManager != "王登峰" or _7DayYearlyProfit < 3 or _10kProfit < 1:
        	print "warning..."
        	content = "基金经理：" + fundManager + "\n"
        	content += "万份收益：" + str(_10kProfit) + "元\n"
        	content += "7日年化收效率" + str(_7DayYearlyProfit) + "%\n"
        	send_simple_message(content)
        