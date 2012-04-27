#!/usr/bin/python
#encoding=utf8

import sys, os.path

if __name__ == "__main__":
	if len(sys.argv)!=3:
		print "usage: ", os.path.basename(__file__), "<dir_a> <dir_b>"
	else:
		pathA = sys.argv[1]
		pathB = sys.argv[2]

        if not os.path.exists(pathA):
            print "error:", pathA, "doesn't exist!"
            sys.exit(-1)
        if not os.path.exists(pathB):
            print "error:", pathB, "doesn't exist!"
            sys.exit(-1) 

        for root, dirs, files in os.walk(pathA):
            for file in files:
                print os.path.join(root, file)
