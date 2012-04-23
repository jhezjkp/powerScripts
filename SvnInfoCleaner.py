#!/usr/bin/python
#encoding=utf8

'''
该脚本用于清理脚本所在目录下SVN信息
'''

import os, shutil

for root, dirs, files in os.walk("."):
    for dir in dirs:
        if dir==".svn":
            path = os.path.join(root, dir)
            print "deleting", path
            shutil.rmtree(path)
            
