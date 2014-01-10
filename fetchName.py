#!/usr/bin/env python
#encoding=utf-8


import requests
from bs4 import BeautifulSoup


def fetch_names(url_pattern, pages=1):
	name_list = list()	
	page = 1
	while page <= pages:
		url = url_pattern % page
		r = requests.get(url)
		if r.status_code == 200:
			print "正在采集" + url + "..."
			soup = BeautifulSoup(r.text)						
			for item in soup.find_all("a", "js-vip-check"):
				name = item.get("uname")
				if name and len(name.strip()) > 0 and name.strip() not in name_list:
					name_list.append(name.strip())			
		page += 1
	f = file('names.txt', 'w')
	for name in name_list:
		f.write(name+"\n")
	f.close()
	print "共采集了%d个名字" % len(name_list)

if __name__ == '__main__':
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')	
	fetch_names("http://bbs.tianya.cn/post-free-3676588-%d.shtml", 391)
