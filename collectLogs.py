#!/usr/bin/python
#encoding=utf-8

'''
日志收集
'''

import sys
import os
import time
import datetime
import glob
import logging
import socket
import cPickle
import threading
import struct
import hashlib
import Queue
from xml.dom import minidom, Node

#日志记录器
logger = None
#日志存储目录
logPath = "/home/tx/collector"
########服务器配置###########
#日志存放目录(默认为程序所在的目录)
targetPath = os.path.dirname(os.path.abspath(__file__))
#监听端口
port = 19200
########客户端配置##########
#上传时大大线程数
maxThread = 5
#发送队列
sendQueue = Queue.Queue()
#服务端地址和端口
remoteHost = "192.168.1.244"
remotePort = 19200


def receiveData(clientfd):
    clientReader = clientfd.makefile("rb")
    md5 = hashlib.md5()
    while True:
        # 接收数据包的大小（4个字节的int）
        data = clientReader.read(4)
        if len(data) !=4:
            break
        dataLength = struct.unpack("I", data)[0]
        data = clientReader.read(dataLength)
        packet = cPickle.loads(data)
        path = os.path.join(targetPath, packet["path"])
        #print targetPath, path, packet["path"]
        # 递归创建目录
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.makedirs(parent)
        file(path, "wb").write(packet["data"])
        logger.info("Received file: %s", path)
        md5.update(file(path, "rb").read())
        if packet['md5'] !=md5.hexdigest():
            logger.error("文件一致性校验失败: %s\t%s\t%s",
                path, packet['md5'], md5.hexdigest())
        #print packet['md5'], md5.hexdigest()
        #如果接收到的是7z压缩文件，则解压之
        if path.endswith('.7z'):
            os.chdir(os.path.dirname(path))
            print '7z -y x ', os.path.basename(path)
            os.system('7z -y x \"' +os.path.basename(path)+'\" > /dev/null')
        clientfd.send('\xff')


def startServer():
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置重用标记，这样重启程序的时候不会提示端口被占用。
    fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    fd.bind(("", port))
                # 连接等待队列的最大容量设置为5
    fd.listen(5)
    while True:
        # 等待客户端连接
        clientfd, addr = fd.accept()
        thread = threading.Thread(target= receiveData, args = (clientfd, ))
        # 设置Daemon属性可以让server结束，则所有子线程必须也退出
        thread.setDaemon(True)
        thread.start()


class Server:
    '''
    游戏服配置bean
    '''
    def __init__(self, label, name, path, logs):
        self.label = label
        self.name = name
        self.path = path
        self.logs = logs

    def __str__(self):
        return "%s[%s-%s]" % (self.label, self.name, self.path)


def loadConfig():
    '''
    返回一个key为name、value为游戏服配置的字典
    '''
    xmldoc = minidom.parse(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config_collectLogs.xml"))
    gameLogs = []
    nodeList = xmldoc.firstChild.getElementsByTagName(
        "gameLogs")[0].getElementsByTagName("log")
    for node in nodeList:
        gameLogs.append(node.firstChild.data)
    loginLogs = []
    nodeList = xmldoc.firstChild.getElementsByTagName(
        "loginLogs")[0].getElementsByTagName("log")
    for node in nodeList:
        loginLogs.append(node.firstChild.data)
    #print len(gameLogs), len(loginLogs)
    nodeList = xmldoc.firstChild.getElementsByTagName("server")
    servers = {}
    for node in nodeList:
        param = {}
        for n in node.childNodes:
            if n.nodeType == Node.ELEMENT_NODE:
                param[n.nodeName] = n.firstChild.data
        server = Server(param["label"], param["name"], param["path"],
            param["name"].startswith("login") and loginLogs or gameLogs)
        servers[server.name] = server
        #print server
    return servers


def initLogger(logFile):
    '''
    初始化日志配置
    '''
    logger = logging.getLogger()
    logFormat = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(logFormat)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormat)
    logger.addHandler(consoleHandler)

    logger.setLevel(logging.INFO)
    return logger


def gatherLogs(server, start=None, end=None):
    logger.info("gather log from [%s]", server.label)
    logPath = os.path.join(server.path, "log")
    if not os.path.exists(logPath):
        logger.error(
            "log path(%s) for %s doesn't exist!", server.path, server.label)
    else:
        patterns = []
        if start ==None and end==None:
            now = datetime.datetime.now()
            now -= datetime.timedelta(days=1)
            patterns.append(now.strftime("%Y-%m-%d"))
        elif start !=None and end==None:
            patterns.append(start.strftime("%Y-%m-%d"))
        else:
            for i in range(0, (end -start).days+1):
                patterns.append(
                    (start + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        list = []
        count = 0
        for pattern in patterns:
            list += glob.glob(os.path.join(logPath, pattern +"*"))
        for log in list:
            if os.path.basename(log)[10:] in server.logs:
                sendQueue.put(log)
                count += 1
    logger.info("%d logs gathered from [%s]", count, server.label)


def sendLogs(server):
    '''
    将队列中的日志发送到服务器端
    '''
    logger.info("开始传输[%s]日志到服务器...", server.label)
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect((remoteHost, remotePort))
    md5 = hashlib.md5()
    while True:
        try:
            path = sendQueue.get_nowait()
        except:
            return
        target = os.path.join(server.name, path[len(os.path.join(server.path, "log")) +1:].lstrip("/"))
        #print target
        data = file(path, "rb").read()
        md5.update(data)
        packet = {"path": target, "data" : data, "md5" : md5.hexdigest()}
        data = cPickle.dumps(packet)
        fd.send(struct.pack("I", len(data)))
        fd.send(data)
        replyCode = fd.recv(1)
        if replyCode[0] != '\xff':
            print "Failed to send file", path

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    if len(sys.argv) < 2:
        print "Usage: python", __file__, "<client|server>"
        sys.exit(-1)
    elif sys.argv[1] == "client":
        logger = initLogger(os.path.join(logPath, "client.log"))
        servers = loadConfig()
        start = None
        end = None
        try:
            if len(sys.argv) >=3:
                start = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
            if len(sys.argv) >=4:
                end = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d")
        except ValueError:
            print "日期格式错误，正式格式应为\"YYYY-mm-dd\""
            exit()
        for server in servers.values():
            gatherLogs(server, start, end)
            if sendQueue.empty():
                logger.info("[%s]无日志需要传输", server.label)
                continue
            sendLogs(server)
            logger.info("[%s]日志传输完成", server.label)
    elif sys.argv[1] == "server":
        logger = initLogger(os.path.join(logPath, "server.log"))
        try:
            startServer()
        except KeyboardInterrupt:
            exit()
