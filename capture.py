from cv2 import *
import numpy as np

# initialize the camera
cam = VideoCapture(1)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
	namedWindow("cam-test",100)
	imshow("cam-test",img)
	waitKey(0)
	destroyWindow("cam-test")
	imwrite("board.jpg",img) #save image

