#!/bin/python
#encoding=utf-8

'''
一个通用的辅助工具类
'''

import sys

def hilite(msg, status, bold):
    if sys.platform.startswith('linux') and sys.stdout.isatty():
        attrs = []
        if status:
            #绿色
            attrs.append('32')
        else:
            #红色
            attrs.append('31')
        if bold:
            attrs.append('1')
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attrs), msg)
    else:
        return msg

if __name__=='__main__':
    print hilite('helpers test', True, True)
    
