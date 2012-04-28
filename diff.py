#!/usr/bin/python
#encoding=utf-8

import sys, os.path, hashlib

def md5(filePath):
	'''
	�����ļ�md5ֵ
	'''
	md5 = hashlib.md5()
	with open(filePath) as f:
		for line in f:
			md5.update(line)
	return md5.hexdigest()
	
def hashFiles(path):
	'''
	����·���������ļ��Ĺ�ϣֵ�����ؽ��map
	'''
	map = {}
	for root, dirs, files in os.walk(path):
		for file in files:
			path = os.path.join(root, file)
			if file in map:	#��ͬ���ļ�
				print "����ͬ���ļ���", file
				sys.exit(-1)
			else:
				map[file] = md5(path)
	return map

if __name__ == "__main__":
	if len(sys.argv)!=3:
		print "usage: python", os.path.basename(__file__), "<dir_a> <dir_b>"
		sys.exit(-1)
	else:
		pathA = sys.argv[1]
		pathB = sys.argv[2]
		
		#ȷ��ָ����·��������
		if not os.path.exists(pathA):
		  print "error:", pathA, "doesn't exist!"
		  sys.exit(-1)
		if not os.path.exists(pathB):
		  print "error:", pathB, "doesn't exist!"
		  sys.exit(-1) 
		
		#����·���µ��ļ�md5ֵ
		mapA = hashFiles(pathA)
		mapB = hashFiles(pathB)
		
		#�Ƚ���ͬ
		diffList = []
		commonKeys = mapA.viewkeys() & mapB.viewkeys()
		for key in commonKeys:
			if mapA[key]!=mapB[key]:
					diffList.append(key)
		setxorList = mapA.viewkeys() ^ mapB.viewkeys()
		
		#��ʾ�ȽϽ��
		if len(diffList)==0 and len(setxorList)==0:
			print pathA+"��"+pathB+"�е��ļ���ȫһ��"
		else:			
			print "%-35s\t%32s\t%32s" % ("", pathA, pathB)
			for file in diffList:
				print "%-35s\t%32s\t%32s" % (file, mapA[file], mapB[file])
			for file in setxorList:
				print "%-35s\t%32s\t%32s" % (file, mapA.get(file, 'x'), mapB.get(file, 'x'))
			
		
				  	