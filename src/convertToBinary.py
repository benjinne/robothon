from cv2 import *
import numpy as np

img = imread("board.jpg", IMREAD_COLOR)

def top(img):
	h,w = img.shape
	for y in range(h):
		for x in range(w):
			if(img[y, x] == 255):
				return y

def bottom(img):
	h,w = img.shape
	for y in range(h):
		for x in range(w):
			if(img[h-y-1, x] == 255):
				return h-y-1
				
def middleSeperation(img):
	left = 0
	right = 0
	middle = int((bottom(img) + top(img)) / 2)
	h,w = img.shape
	for x in range(w):
		if(img[middle, x] == 255):
			left = x
			break;
	for x in range(w):
		if(img[middle, w-x-1] == 255):
			right = w-x-1
			break
	return right-left	
	
#returns true or false
def isO(img):
	if(middleSeperation(img) > 45):
		print('o')
		return 2
	else:
		print('x')
		return 1

def isEmpty(board):
	for y in range(3):
		for x in range(3):
			if(board[y][x] == 0):
				return True
	return False
			
#returns 0 if no winner, 1 if x wins, 2 if o wins
def check(board):
	testx = 0;
	testo = 0;
	won = 0;
	#test rows
	for y in range(3):
		for x in range(3):
			if(board[y][x] == 1):
				testx += 1
			else:
				testx = 0
			if(board[y][x] == 2):
				testo += 1
			else:
				testo = 0
		if(testx == 3):
			return 1
		elif(testo == 3):
			return 2
		else:
			testx = 0
			texto = 0
			
			
	#test columns
	for x in range(3):
		for y in range(3):
			if(board[y][x] == 1):
				testx += 1
			else:
				testx = 0
			if(board[y][x] == 2):
				testo += 1
			else:
				testo = 0
		if(testx == 3):
			return 1
		elif(testo == 3):
			return 2
		else:
			testx = 0
			testo = 0
			
	#test diagonals
	if(board[0][0] == 1 and board[1][1] == 1 and board[2][2] == 1):
		return 1
	elif(board[0][0] == 2 and board[1][1] == 2 and board[2][2] == 2):
		return 2
	elif(board[0][2] == 1 and board[1][1] == 1 and board[2][0] == 1):
		return 1
	elif(board[0][2] == 2 and board[1][1] == 2 and board[2][0] == 2):
		return 2
	return 0

#places x in board
#def robots_turn(board):
#	for y in range(3):
#		for x in range(3):
#			if(board[y][x]):
			#nothing yet

bw = Canny(img, 30, 150)

crop1 = bw[ 40:170  , 90:210  ]
crop2 = bw[ 40:170  , 240:370 ]
crop3 = bw[ 40:170  , 395:540 ]

crop4 = bw[ 215:320 , 90:210  ]
crop5 = bw[ 215:320 , 240:370 ]
crop6 = bw[ 215:320 , 395:540 ]

crop7 = bw[ 365:475 , 90:210  ]
crop8 = bw[ 365:475 , 240:370 ]
crop9 = bw[ 365:475 , 395:540 ]

w, h = 3, 3;
board = [[0 for x in range(w)] for y in range(h)]
board[0][0] = isO(crop1)
board[0][1] = isO(crop2)
board[0][2] = isO(crop3)
board[1][0] = isO(crop4)
board[1][1] = isO(crop5)
board[1][2] = isO(crop6)
board[2][0] = isO(crop7)
board[2][1] = isO(crop8)
board[2][2] = isO(crop9)

print(isEmpty(board))

imshow("benlinne", bw)
waitKey(0)
destroyWindow("benlinne")

