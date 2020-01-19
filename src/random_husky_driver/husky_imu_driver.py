#!/usr/bin/env python

import rospy, tf
import geometry_msgs.msg, nav_msgs.msg
from math import *
from time import sleep
from sensor_msgs.msg import Imu

def huskyOdomCallback(message,cargs):
	# Implementation of proportional position control 
    # For comparison to Simulink implementation
	yaw = data.orientation.z
	print "Yaw" +str(yaw)
	msg.linear.x = 2
    pub.publish(msg)
    
########################################
# Main Script
# Initialize our node
rospy.init_node('husky_imu_driver',anonymous=True)
    
# Set waypoint for Husky to drive to
goal = [4,2]  # Goal

# Setup publisher
cmdmsg = geometry_msgs.msg.Twist()
cmdpub = rospy.Publisher('/cmd_vel',geometry_msgs.msg.Twist, queue_size=10)

# Setup subscription - which implemets our controller.
# We pass the publisher, the message to publish and the goal as 
# additional parameters to the callback function.
rospy.Subscriber('odometry/filtered',nav_msgs.msg.Odometry,huskyOdomCallback, 
                 (cmdpub,cmdmsg,goal))

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()