#!/usr/bin/python
#encoding=utf-8

import sys
import os.path
import hashlib

from helpers import hashFile, hilite

def hashFiles(path):
	'''
	计算路径下所有文件的哈希值，返回结果map
	'''
	map = {}
	for root, dirs, files in os.walk(path):
		for file in files:
			path = os.path.join(root, file)
			if file in map:	#有同名文件
				print "发现同名文件：", file
				sys.exit(-1)
			else:
				map[file] = hashFile(path)
	return map

if __name__ == "__main__":
	if len(sys.argv)!=3:
		print "usage: python", os.path.basename(__file__), "<dir_a> <dir_b>"
		sys.exit(-1)
	else:
		pathA = sys.argv[1]
		pathB = sys.argv[2]

		reload(sys)
		sys.setdefaultencoding('utf-8')
		#确认指定的路径都存在
		if not os.path.exists(pathA):
		  print "error:", pathA, "doesn't exist!"
		  sys.exit(-1)
		if not os.path.exists(pathB):
		  print "error:", pathB, "doesn't exist!"
		  sys.exit(-1) 
	
		#计算路径下的文件md5值
		mapA = hashFiles(pathA)
		mapB = hashFiles(pathB)
	
		#比较异同
		diffList = []
		commonKeys = mapA.viewkeys() & mapB.viewkeys()
		for key in commonKeys:
			if mapA[key]!=mapB[key]:
					diffList.append(key)
		setxorList = mapA.viewkeys() ^ mapB.viewkeys()

		#显示比较结果
		if len(diffList)==0 and len(setxorList)==0:
			print pathA+"与"+pathB+"中的文件"+hilite("完全一致")
		else:			
			print "%-35s\t%32s\t%32s" % ("", pathA, pathB)
			for file in diffList:
				print "%-35s\t%32s\t%32s" % (file, mapA[file], mapB[file])
			for file in setxorList:
				print "%-35s\t%32s\t%32s" % (file, mapA.get(file, 'x'), mapB.get(file, 'x'))
			
		
				  	
