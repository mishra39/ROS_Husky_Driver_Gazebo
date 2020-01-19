#!/usr/bin/env python
# <!-- <node name="$(anon main)" pkg="clifford_package" type="main4_PD_imu.py" /> -->
import rospy, tf
import geometry_msgs.msg, nav_msgs.msg
from math import *
import math
from time import sleep
from sensor_msgs.msg import Imu
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu

def huskyOdomCallback(message,cargs):

    # Implementation of proportional position control 
    # For comparison to Simulink implementation

    # Callback arguments 
    pub,msg,goal = cargs
    
    # Publish
    msg.linear.x = 2
    
    Kp = -50
    Kd = -10
    if len(yaw_err_arr) > 1:
        msg.angular.z = Kp*yaw_err + Kd*(yaw_err_arr[1]-yaw_err_arr[0])*0.1
    pub.publish(msg)
    print "Yaw (heading) angle error(rad)= " + str(yaw_err)

def ImuCallback(data):
	global yaw_des
	global yaw_err
    
	yaw = data.orientation.z
	
	yaw_des = 0
	yaw_err = yaw - yaw_des
    yaw_err_arr.append(yaw_err)

	print "Yaw Added",len(yaw_err_arr)
    
########################################
# Main Script
# Initialize our node
global yaw_err_arr
yaw_err_arr = []

rospy.init_node('huskycontrol',anonymous=True)
    
# Set waypoint for Husky to drive to
goal = [4,2]  # Goal

# Setup publisher
sub_imu = rospy.Subscriber('/imu/data',Imu,ImuCallback)
cmdmsg = geometry_msgs.msg.Twist()
cmdpub = rospy.Publisher('/cmd_vel',geometry_msgs.msg.Twist, queue_size=10)

# Setup subscription - which implemets our controller.
# We pass the publisher, the message to publish and the goal as 
# additional parameters to the callback function.
rospy.Subscriber('odometry/filtered',nav_msgs.msg.Odometry,huskyOdomCallback, 
                 (cmdpub,cmdmsg,goal))


# spin() simply keeps python from exiting until this node is stopped
rospy.spin()