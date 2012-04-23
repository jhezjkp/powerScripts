#!/usr/bin/python
#encoding=utf8

'''
该脚本用于清理脚本所在目录下SVN信息
'''

import sys, os, shutil, stat

def on_rm_error(func, path, exc_info):
    '''
    解决windows下因目录只读属性导致删除失败的情况
    '''
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

for root, dirs, files in os.walk("."):
    for dir in dirs:
        if dir==".svn":            
            path = os.path.join(root, dir)
            print "deleting", path
            try:
                shutil.rmtree(path, onerror=on_rm_error)
            except:
                info = sys.exc_info()
                print info[0], ":", info[1]
            
