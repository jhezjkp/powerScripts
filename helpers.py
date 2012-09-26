#!/bin/python
#encoding=utf-8

'''
一个通用的辅助工具类
'''

import sys
import os.path
import datetime
from functools import wraps
import hashlib

from colorama import Fore, Back, Style, init

#init colorama
init()


def hilite(msg, foreColor=Fore.WHITE, backColor=Back.GREEN, style=Style.BRIGHT):
    '''console文字高亮'''
    if sys.stdout.isatty():
        return foreColor + backColor + style + msg + Style.RESET_ALL
    else:
        return msg


class DirHashUnavaliableException(Exception):
    '''目录哈希值计算不可用异常(暂不支持目录的哈希计算)'''
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "暂时不支持对目录的希值计算"


def hashFile(filePath, algorithm='md5'):
    '''计算文件哈希值，默认为md5算法'''
    if not os.path.exists(filePath):
        raise IOError("No such file: '" + filePath + "'")
    elif os.path.isdir(filePath):
        raise DirHashUnavaliableException()
    h = hashlib.new(algorithm)
    with open(filePath) as f:
        for line in f:
            h.update(line)
    return h.hexdigest()


class MyTimer:
    '''
    方法执行时间测量
    '''

    def __init__(self):
        pass

    def __call__(self, f):
        @wraps(f)
        def _decorated(*args, **kw):
            try:
                start = datetime.datetime.now()
                result = f(*args, **kw)
                end = datetime.datetime.now()
                print f.__name__ + '():', end - start
            except Exception:
                pass
            return result
        return _decorated


if __name__ == '__main__':
    print 'hilite:', hilite('customise hilite', Fore.RED, Back.WHITE, Style.DIM), 'and', hilite('default hilite')
    print "md5(" + __file__ + ")", hashFile(__file__)
    print "sha1" + __file__ + ")", hashFile(__file__, 'sha1')
    print "sha224(" + __file__ + ")", hashFile(__file__, 'sha224')
    print "sha256(" + __file__ + ")", hashFile(__file__, 'sha256')
    print "sha384(" + __file__ + ")", hashFile(__file__, 'sha384')
    print "sha512(" + __file__ + ")", hashFile(__file__, 'sha512')
    try:
        hashFile('/tmp')
    except:
        info = sys.exc_info()
        print info[0], ":", info[1]
    try:
        hashFile('/nonexist/file')
    except:
        info = sys.exc_info()

    print '================'
    myTimer = MyTimer()

    import time
    import random

    @myTimer
    def say(str):
        time.sleep(random.randint(0, 10))
        print str

    say('abc')
    say('你妹')
