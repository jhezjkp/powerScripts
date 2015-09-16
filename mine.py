#/usr/bin/env python
#encoding=utf-8


"""
a simple mine game
"""

import sys
import random

width = 4
height = 5

mine_count = 0

#mire grid, ignore shadow copy
grid = [([0] * width) for i in range(height)]
#marked as blank grid
marked = []
#auto blank grid
auto_blank = []


def display_grid(mode=0):
	for i in range(0, len(grid)):
		for j in range(0, len(grid[i])):
			if mode == 0:
				print grid[i][j], "\t",
			elif mode == 1:
				if (i * width + j) in marked or (i * width + j) in auto_blank:
					print get_label(i, j), "\t",
				else:
					print "#", "\t",
			elif mode == 2:
				if (i * width + j) == marked[len(marked) -1]:
					print "[" + str(grid[i][j]) + "]", "\t",
				else:
					print grid[i][j], "\t",
		print ""

def deploy_mines():
	#deploy mines
	global mine_count
	mine_count = random.randint(1, width * height / 2)
	#print mine_count, "mines to be deploy..."
	deploy_count = 0
	while deploy_count < mine_count:
		i = random.randint(0, height - 1)
		j = random.randint(0, width -1)
		#print i, j, grid[i][j]
		if grid[i][j] == 0:
			grid[i][j] = 1
			deploy_count += 1
			#display_grid()
			#print "dploy [ "+ str(i), ",", str(j)+" ]", deploy_count
			#print "----------------------"
	#print "done"


def get_label(x, y):
	label = 0
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			m = x + i
			n = y + j
			if m < 0 or n <0 or m > (height - 1) or n > (width - 1)  or (m == x and n == y):
				continue
			elif grid[m][n] == 1:
				label += 1
	return label


def auto_blank_check(x, y):
	label = get_label(x, y)
	#print "check ", x, y, label
	if label == 0:
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				m = x + i
				n = y + j
				if m < 0 or n <0 or m > (height - 1) or n > (width - 1)  or (m == x and n == y) or (m * width + n) in auto_blank:
					continue
				elif get_label(m, n) == 0:
					auto_blank.append(m * width + n)
					auto_blank_check(m, n)
				else:
					auto_blank.append(m * width + n)


def mark_mine():
	mark = int(raw_input("Plear mark a blank grid(0~" + str(width * height - 1) + "): "))
	if mark in marked:
		print "already marked!!!"
		return mark_mine()
	elif mark > width * height - 1:
		print "too large!!!"
		return mark_mine()
	marked.append(mark)
	#print "--->",  width * height - len(marked), mine_count
	if grid[mark / width][mark % width] == 1:
		print "game over"
		print "--------------------"
		display_grid(2)
	elif width * height - len(marked) - len(auto_blank) != mine_count:
		auto_blank_check(mark / width, mark % width)
		print "----------------"
		print marked
		display_grid(1)
		mark_mine()
	else:
		print "========== success =========="
		print "your mark:", marked
		display_grid()

reload(sys)
sys.setdefaultencoding("gbk")
deploy_mines()
display_grid(1)
mark_mine()
