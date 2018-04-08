#!/usr/bin/env python

import rospy
from cv2 import *
import numpy as np
import actionlib
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from control_msgs.msg import *

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
rospy.init_node('bens_node', anonymous=True, disable_signals=True)
my_client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
succ = my_client.wait_for_server(timeout=rospy.Duration(10))

board1 = [-3.4229443709002894, -1.7821601072894495, 2.718715190887451, -0.966079060231344, 1.4054919481277466, 0.02844718098640442]
board2 = [-3.2743313948260706, -1.6557133833514612, 2.6738076210021973, -0.9783909956561487, 1.4991707801818848, 0.02839924395084381]
board3 = [-3.2103965918170374, -1.693007771168844, 2.58252215385437, -0.9229639212237757, 1.4482475519180298, 0.012366222217679024]
board4 = [-3.138555351887838, -1.603715721760885, 2.467524528503418, -0.8437069098102015, 1.6489073038101196, 0.012354237958788872]
board5 = [-3.2739718596087855, -1.3821218649493616, 2.4250476360321045, -0.9994705359088343, 1.4368269443511963, 0.028375275433063507]
board6 = [-3.3636329809771937, -1.4404061476336878, 2.455526828765869, -1.0181906859027308, 1.3702448606491089, 0.0280277319252491]
board7 = [-3.4527443091021937, -1.652250115071432, 2.4688668251037598, -0.6950834433185022, 1.4122941493988037, 0.012701780535280704]
board8 = [-3.5628631750689905, -1.7930658499347132, 2.6133053302764893, -0.819671932850973, 1.1924992799758911, 0.01258193887770176]
boardup = [-3.3740573565112513, -1.8141472975360315, 2.407045841217041, -0.6599496046649378, 1.3523688316345215, 0.01261789072304964]
camera = [-3.2671666781054896, -1.4993389288531702, 2.3634088039398193, -0.029624287282125294, 1.7136157751083374, 0.9688253402709961]

def moveto(new_pose):
	g = FollowJointTrajectoryGoal()
	g.trajectory = JointTrajectory()
	g.trajectory.joint_names = JOINT_NAMES
	joint_states = rospy.wait_for_message('/joint_states', JointState)
	joint_pos = joint_states.position
	g.trajectory.points = [
		JointTrajectoryPoint(positions=joint_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
		JointTrajectoryPoint(positions=new_pose, velocities=[0]*6, time_from_start=rospy.Duration(2.0))
	]
	my_client.send_goal(g)
	my_client.wait_for_result()

def takePic():
	# initialize the camera
	cam = VideoCapture(0)   # 0 -> index of camera
	s, img = cam.read()
	s, img = cam.read()
	
	bw = Canny(img, 30, 150)
	
	if s:    # frame captured without any errors
		namedWindow("cam-test",100)
		imshow("cam-test",bw)
		imwrite("board.jpg",bw) #save image
	return bw

##########################################################################################################

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
	
##########################################################################################################
	
if succ:
	game = True
	
	moveto(boardup)
	moveto(board1)
	moveto(board6)
	moveto(boardup)
	moveto(board2)
	moveto(board5)
	moveto(boardup)
	moveto(board8)
	moveto(board3)
	moveto(boardup)
	moveto(board7)
	moveto(board4)
	moveto(boardup)
	waitKey(0)
	
	w, h = 3, 3;
	board = [[0 for x in range(w)] for y in range(h)]
	
	while(game):
		if(isEmpty()):
			game = false
			result = check()
			if(check == 0):
				print("tie")
			elif(check == 1):
				print("x,bot WON!")
			elif(check == 2):
				print("o, user WON!")
			break;
		
		moveto(camera)
		bw = takePic()
		board[0][0] = isO(crop1)
		board[0][1] = isO(crop2)
		board[0][2] = isO(crop3)
		board[1][0] = isO(crop4)
		board[1][1] = isO(crop5)
		board[1][2] = isO(crop6)
		board[2][0] = isO(crop7)
		board[2][1] = isO(crop8)
		board[2][2] = isO(crop9)
		
		
		
		
		
else:
	print "uh oh!"
