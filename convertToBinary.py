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

#returns 'x' or 'o'
def x_or_o(img):
	if(middleSeperation(img) < 15):
		return 'x'
	else:
		return 'o'

bw = Canny(img, 30, 150)

crop1 = bw[ 50:170  , 75:210  ]
crop2 = bw[ 50:170  , 230:345 ]
crop3 = bw[ 60:180  , 365:480 ]
crop4 = bw[ 190:310 , 75:205  ]
crop5 = bw[ 195:310 , 230:340 ]
crop6 = bw[ 200:320 , 365:480 ]
crop7 = bw[ 330:470 , 85:210  ]
crop8 = bw[ 330:470 , 230:340 ]
crop9 = bw[ 335:455 , 360:470 ]


print(x_or_o(crop1))
print(x_or_o(crop2))
print(x_or_o(crop3))
print(x_or_o(crop4))
print(x_or_o(crop5))
print(x_or_o(crop6))
print(x_or_o(crop7))
print(x_or_o(crop8))
print(x_or_o(crop9))

imshow("benlinne", bw)
waitKey(0)
destroyWindow("benlinne")

