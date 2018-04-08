#!/usr/bin/env python

import rospy

import actionlib
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from control_msgs.msg import *

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
rospy.init_node('bens_node', anonymous=True, disable_signals=True)
my_client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
succ = my_client.wait_for_server(timeout=rospy.Duration(10))

if succ:
	g = FollowJointTrajectoryGoal()
	g.trajectory = JointTrajectory()
	g.trajectory.joint_names = JOINT_NAMES

	joint_states = rospy.wait_for_message('/joint_states', JointState)
	joint_pos = joint_states.position

	my_pose = [-3.0753055254565638, -1.2640836874591272, 2.018401622772217, -0.7003157774554651, 1.7759090662002563, -0.051656548176900685]

	g.trajectory.points = [
		JointTrajectoryPoint(positions=joint_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
		JointTrajectoryPoint(positions=my_pose, velocities=[0]*6, time_from_start=rospy.Duration(2.0))
	]

	my_client.send_goal(g)
	my_client.wait_for_result()
	
	
	
	
else:
	print "uh oh!"