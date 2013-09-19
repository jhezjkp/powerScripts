#!/usr/bin/env python

"""
https://www.elance.com/j/duplicate-file-finder-mac-os/46892675/?backurl=aHR0cHM6Ly93d3cuZWxhbmNlLmNvbS9yL2pvYnMvY2F0LWl0LXByb2dyYW1taW5nL3NjdC13ZWItcHJvZ3JhbW1pbmctMTAyMjQtc29mdHdhcmUtYXBwbGljYXRpb24tMTAyMTYtc3lzdGVtLWFkbWluaXN0cmF0aW9uLTEwMjE5LWRhdGFiYXNlLWRldmVsb3BtZW50LTEwMjE3L3AtMz9zZWFyY2hJZD01MjM5NTY=

hi,

i want a application for Mac OS, to find duplicate files/images/music etc...

it should support Mac 10.6 to 10.9 (latest) with bug free
"""

import os
import os.path
import hashlib
import re
import string

#target path to find duplicate files
#path = "/Users/vivia/duplicate"
path = "/Volumes/data"
#suffixes to be checked
#filters = ["jpg", "mp3", "avi"]
filters = ["png", "jpg", "mp3", "avi"]
#result map: key-fmd5 valu value-file path
map = {}

pattern = re.compile(string.join(filters, "$|") + "$")


def hash_file(path, algorithm="md5", blocksize=65535):
    '''calculate file value using md5 algorithm'''
    if not os.path.exists(path):
        raise IOError("No such file: '" + path + "'")
    elif os.path.isdir(path):
        raise IOError("Can't calculate on a folder!")
    h = hashlib.new(algorithm)
    afile = open(path, 'rb')
    buf = afile.read(blocksize)
    while len(buf) > 0:
        h.update(buf)
        buf = afile.read(blocksize)
    return h.hexdigest()

resultFile = open("result.txt", "w")

for root, dirs, files in os.walk(path):
    for f in files:
        if not pattern.search(f):
            continue
        fullPath = os.path.join(root, f)
        md5_value = hash_file(fullPath)
        if md5_value in map:
            print "duplicate file found:", fullPath, map[md5_value]
            resultFile.writelines(fullPath + "\t" + map[md5_value] + "\n")
        else:
            map[md5_value] = fullPath
