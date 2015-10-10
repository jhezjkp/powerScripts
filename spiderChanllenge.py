#!/usr/bin/env python
# encoding=utf-8

import sys
import threading
import re
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


def changlenge1():
    url = "http://www.heibanke.com/lesson/crawler_ex00/"
    n = ""
    while True:
        print "scrap page ", url + n
        r = requests.get(url + n)
        if r.status_code == 200:
            if r.content.find("答案") == -1:
                bs = BeautifulSoup(r.content, "html.parser")
                s = bs.find_all("h3")[0].text
                try:
                    n = re.search(r"\d+", s).group(0)
                except:
                    print s
                    print url + n
                    break
            else:
                print r.text
                break


def changlenge2():
    url = "http://www.heibanke.com/lesson/crawler_ex01/"
    n = 0
    while True:
        print "try password:", n
        data = {"username": "kvs", "password": n}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            if r.content.find("您输入的密码错误") != -1:
                n += 1
                continue
            else:
                print "password is: ", n
                print r.text
                break


def changlenge3():
    s = requests.Session()
    # login first
    loginUrl = "http://www.heibanke.com/accounts/login"
    r = s.get(loginUrl)
    if r.status_code == 200:
        # print r.text
        bs = BeautifulSoup(r.text, "html.parser")
        csrf = bs.find_all("input")[0]["value"]
        print csrf
        # print r.cookies
        data = {"username": "kvvs", "password": "123456",
                "csrfmiddlewaretoken": csrf}
        r = s.post(loginUrl + "/?next=/lesson/crawler_ex02/",
                   data=data, allow_redirects=True)
        # print r.status_code
        # print r.text
        print r.url
        print "----------------------------"
        bs = BeautifulSoup(r.text, "html.parser")
        csrf = bs.find_all("input")[0]["value"]
        print csrf

        url = "http://www.heibanke.com/lesson/crawler_ex02/"
        n = 0
        while True:
            print "try password:", n
            data = {"username": "kvvs", "password": n,
                    "csrfmiddlewaretoken": csrf}
            r = s.post(url, data=data)
            if r.status_code == 200:
                if r.content.find("您输入的密码错误") != -1:
                    n += 1
                    # print r.text
                    continue
                else:
                    print "password is: ", n
                    print r.text
                    bs = BeautifulSoup(r.text, "html.parser")
                    break
            else:
                print r.text

class Task(threading.Thread):

    def __init__(self, s, url, csrf, i):
        super(Task, self).__init__()
        self.name = "thread-" + str(i)
        self.s = s
        self.url = url
        self.csrf = csrf
        self.i = i

    def run(self):
        n = 0
        while not sig.is_set():
            if n % total != self.i:
                continue
            print self.name, "try password:", n
            data = {"username": "kvvs", "password": n,
                    "csrfmiddlewaretoken": self.csrf}
            r = self.s.post(self.url, data=data)
            if r.status_code == 200:
                if r.content.find("您输入的密码错误") != -1:
                    n += 1
                    # print r.text
                    continue
                else:
                    print "password is: ", n
                    print r.text
                    sig.set()
                    break


def changlenge4():
    s = requests.Session()
    # login first
    loginUrl = "http://www.heibanke.com/accounts/login"
    r = s.get(loginUrl)
    if r.status_code == 200:
        # print r.text
        bs = BeautifulSoup(r.text, "html.parser")
        csrf = bs.find_all("input")[0]["value"]
        print csrf
        # print r.cookies
        data = {"username": "kvvs", "password": "123456",
                "csrfmiddlewaretoken": csrf}
        r = s.post(loginUrl + "/?next=/lesson/crawler_ex03/",
                   data=data, allow_redirects=True)
        # print r.status_code
        # print r.text
        print r.url
        print "----------------------------"
        bs = BeautifulSoup(r.text, "html.parser")
        csrf = bs.find_all("input")[0]["value"]
        print csrf

        url = "http://www.heibanke.com/lesson/crawler_ex03/"
        n = 0
        for i in range(total):
            t = Task(s, url, csrf, i)
            print "start thread", i
            t.start()
        #while True:
            #print "try password:", n
            #data = {"username": "kvvs", "password": n,
                    #"csrfmiddlewaretoken": csrf}
            #r = s.post(url, data=data)
            #if r.status_code == 200:
                #if r.content.find("您输入的密码错误") != -1:
                    #n += 1
                    ## print r.text
                    #continue
                #else:
                    #print "password is: ", n
                    #print r.text
                    #bs = BeautifulSoup(r.text, "html.parser")
                    #break
            #else:
                #print r.text
         #       sys.exit(1)


sig = threading.Event()
total = 10
if __name__ == "__main__":
    changlenge4()
