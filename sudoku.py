# -*- coding: utf-8 -*-
# @Author: Joren Vandeweyer
# @Date:   2017-07-04 19:18:17
# @Last Modified by:   Joren Vandeweyer
# @Last Modified time: 2017-08-07 20:50:25

class Sudoku():
	"""docstring for Sudoku"""
	def __init__(self):
		# self.sudoku = [
		# 	[0,0,0,1,0,4,9,0,0],
		# 	[2,0,3,0,5,7,4,1,0],
		# 	[4,0,0,0,8,2,0,7,0],
		# 	[0,0,4,0,2,0,0,0,1],
		# 	[5,1,0,0,0,0,0,8,6],
		# 	[3,6,0,0,7,1,2,0,0],
		# 	[0,2,0,7,1,0,5,6,4],
		# 	[0,3,5,0,6,8,1,9,2],
		# 	[0,0,6,0,0,5,0,0,0]
		# ]
		# self.sudoku = [
		# 	[0,0,0,1,0,4,8,0,0],
		# 	[2,0,0,0,0,0,0,0,9],
		# 	[0,0,9,0,0,0,1,0,0],
		# 	[0,2,0,0,8,9,6,0,7],
		# 	[0,7,0,0,1,0,0,3,0],
		# 	[9,0,6,4,7,0,0,8,0],
		# 	[0,0,7,0,0,0,2,0,0],
		# 	[4,0,0,0,0,0,0,0,6],
		# 	[0,0,2,5,0,1,0,0,0]
		# ]
		# self.sudoku = [
		# 	[9,0,0,4,0,8,0,0,0],
		# 	[0,0,2,0,0,0,1,0,0],
		# 	[3,0,0,0,0,0,0,0,9],
		# 	[1,0,5,2,3,0,0,6,0],
		# 	[0,3,0,0,8,0,0,7,0],
		# 	[0,9,0,0,6,5,3,0,1],
		# 	[5,0,0,0,0,0,0,0,8],
		# 	[0,0,9,0,0,0,5,0,0],
		# 	[0,0,0,8,0,2,0,0,6]
		# ]
		self.sudoku = [
			[0,0,0,0,0,0,0,0,0],
			[2,7,8,0,0,0,1,6,9],
			[0,0,0,2,0,9,0,0,0],
			[0,3,7,0,5,0,8,4,0],
			[0,0,0,0,0,0,0,0,0],
			[0,5,1,0,6,0,7,3,0],
			[0,0,0,4,0,7,0,0,0],
			[5,9,4,0,0,0,3,7,6],
			[0,0,0,0,0,0,0,0,0]
		]
		self.solve()

	def printSudoku(self):
		for row in self.sudoku:
			print(row)

	def solve(self):
		for i in range(0,9):
			for j in range(0,9):
				if self.sudoku[i][j] == 0:
					pos = possibilities(self.sudoku, i, j)
					if len(pos) == 1:
						self.sudoku[i][j] = pos[0]
					else:
						self.sudoku[i][j] = pos
				elif type(self.sudoku[i][j]) == list:
					if singlePossibility(self.sudoku, i, j):
						pass
					elif lookForInvisibleLines(self.sudoku, i, j):
						pass
				else:
					removePossibilities(self.sudoku, i, j)
					continue
		else:
			if self.complete():
				self.printSudoku()
				print("[+] COMPLETE")
				return
			else:
				self.printSudoku()
				print("--")
				self.solve()

	def complete(self):
		for i in range(0,9):
			for j in range(0,9):
				if self.sudoku[i][j] == 0 or type(self.sudoku[i][j]) == list:
					return False
		else:
			return True

def possibilities(matrix, row, column):
	pos = list(range(1, 10))
	pos = rowPossibilities(matrix, row, pos)
	pos = columnPossibilities(matrix, column, pos)
	pos = blockPossibilities(matrix, row, column, pos)
	return pos

def rowPossibilities(matrix, row, numbers):
	for i in numbers[:]:
		if i in matrix[row]:
			numbers.remove(i)
	else:
		return numbers

def columnPossibilities(matrix, column, numbers):
	matrix = [[row[i] for row in matrix] for i in range(9)]
	for i in numbers[:]:
		if i in matrix[column]:
			numbers.remove(i)
	else:
		return numbers

def blockPossibilities(matrix, row, column, numbers):
	blockRow = createBlockRange(row // 3)
	blockColumn = createBlockRange(column // 3)

	current = []

	for i in blockRow:
		for j in blockColumn:
			if matrix[i][j] != 0:
				current.append(matrix[i][j])

	for i in numbers[:]:
		if i in current:
			numbers.remove(i)
	else:
		return numbers

def removePossibilities(matrix, row, column):
	value = matrix[row][column]
	removeRowPossibilities(matrix, row, value)
	removeColumnPossibilities(matrix, column, value)
	removeBlockPossibilities(matrix, row, column, value)

def removeRowPossibilities(matrix, row, value):
	for column in range(0,9):
		cleanUpList(matrix, row, column, value)

def removeColumnPossibilities(matrix, column, value):
	for row in range(0,9):
		cleanUpList(matrix, row, column, value)

def removeBlockPossibilities(matrix, row, column, value):
	blockRow = createBlockRange(row // 3)
	blockColumn = createBlockRange(column // 3)

	for i in blockRow:
		for j in blockColumn:
			cleanUpList(matrix, i, j, value)

def cleanUpList(matrix, row, column, value):
	l = matrix[row][column]
	if type(l) == list:
		if value in l :
			l.remove(value)
			if len(l) == 1:
				matrix[row][column] = l[0]
				removePossibilities(matrix, row, column)

def createBlockRange(current):

	return range(current * 3, current * 3 + 3)

def lookForInvisibleLines(matrix, row, column):
	for value in matrix[row][column]:
		lookForHorizontalLine(matrix, row, column, value)
		lookForVerticalLine(matrix, row, column, value)
	else: return False

def lookForHorizontalLine(matrix, row, column, value):
	blockRow = createBlockRange(row // 3)
	blockColumn = createBlockRange(column // 3)

	for i in blockRow:
		if i == row:
			continue
		for j in blockColumn:
			if type(matrix[i][j]) == list:
				if value in matrix[i][j]:
					return
			elif matrix[i][j] == value:
				return

	for j in range(0,9):
		if j in blockColumn:
			continue
		else:
			cleanUpList(matrix, row, j, value)

def lookForVerticalLine(matrix, row, column, value):
	blockRow = createBlockRange(row // 3)
	blockColumn = createBlockRange(column // 3)

	for j in blockColumn:
		if j == column:
			continue
		for i in blockRow:
			if type(matrix[i][j]) == list:
				if value in matrix[i][j]:
					return
			elif matrix[i][j] == value:
				return

	for i in range(0,9):
		if i in blockRow:
			continue
		else:
			cleanUpList(matrix, i, column, value)

def singlePossibility(matrix, row, column):
	for value in matrix[row][column]:
		if singleRowPossibility(matrix, row, column, value):
			matrix[row][column] = value
			removePossibilities(matrix, row, column)
			return True
		elif singleColumnPossibility(matrix, row, column, value):
			matrix[row][column] = value
			removePossibilities(matrix, row, column)
			return True
		elif singleBlockPossibility(matrix, row, column, value):
			matrix[row][column] = value
			removePossibilities(matrix, row, column)
			return True
	else:
		return False

def singleRowPossibility(matrix, row, column, value):
	for j in range(0,9):
		if j == column:
			continue
		if type(matrix[row][j]) == list:
			if value in matrix[row][j]:
				return False
		elif value == matrix[row][j]:
			return False
	else:
		return True

def singleColumnPossibility(matrix, row, column, value):
	for i in range(0,9):
		if i == row:
			continue
		if type(matrix[i][column]) == list:
			if value in matrix[i][column]:
				return False
		elif value == matrix[i][column]:
				return False
	else:
		return True

def singleBlockPossibility(matrix, row, column, value):
	blockRow = createBlockRange(row // 3)
	blockColumn = createBlockRange(column // 3)

	for i in blockRow:
		for j in blockColumn:
			if i == row and j == column:
				continue
			if type(matrix[row][column]) == list:
				if value in matrix[row][column]:
					return False
			elif value == matrix[i][j]:
				return False
	else:
		return True

sudoku = Sudoku()
