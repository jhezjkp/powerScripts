#!/usr/bin/env python
#encoding=utf-8

'''
一个辅助工具，方便不熟悉linux命令行的同事做一些日常操作
'''

import os
import sys
import re

#定义服务器
servers = ['10.147.20.224', '10.147.20.225', '10.147.21.78']


def displayMenu():
    '''显示菜单'''
    print "======= general asa assist tool ======"
    print "A: Login to server"
    print "B: Upload files under [/data/MNET/m_meifeng/upload] to percific server"
    print "Q: Quit"
    return raw_input("Your choice:")


def displayServers():
    '''显示可供操作的服务服务器列表'''
    print "====== pls choose a server ======="
    for i in range(len(servers)):
        print str(i + 1) + ": " + servers[i]
    return raw_input("Your choice:")


def getSelectedServer():
    '''获取用户选择的有效服务器'''
    target = ""
    while re.match("^\d+$", target) is None or int(target) <= 0 or int(target) > len(servers):
        target = displayServers()
    return servers[int(target) - 1]


if __name__ == "__main__":
    try:
        while True:
            menu = displayMenu()
            if menu is None or len(menu.strip()) == 0:
                continue
            elif menu.lower() == "q":
                sys.exit(0)
            elif menu.lower() == "a":
                #执行登录命令
                os.system("ssh cp_mqq@" + getSelectedServer())
            elif menu.lower() == "b":
                #执行文件上传命令
                os.system("scp -r /data/MNET/m_meifeng/upload/ cp_mqq@" + getSelectedServer() + ":/usr/local/cp_mqq/update")
    except KeyboardInterrupt:
        print "\nexit..."
        sys.exit(0)
