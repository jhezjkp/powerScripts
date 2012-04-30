#!/bin/python
#encoding=utf-8

'''
一个通用的辅助工具类
'''

import sys
from colorama import Fore, Back, Style, init

#init colorama
init()

def hilite(msg, foreColor=Fore.WHITE, backColor=Back.GREEN, style=Style.BRIGHT):
    '''console文字高亮'''
    if sys.stdout.isatty():
        return foreColor+backColor+style+msg+Style.RESET_ALL
    else:
        return msg

if __name__=='__main__':
    print 'hilite:', hilite('customise hilite', Fore.RED, Back.WHITE, Style.DIM), 'and', hilite('default hilite')
    
