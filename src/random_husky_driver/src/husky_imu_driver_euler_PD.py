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
    
    Kp = -50
    Kd = -10
    yaw_len = len(yaw_err_arr)
    if yaw_len > 2:
    	msg.linear.x = 1
        msg.linear.y = Kp*yaw_err_arr[-1] + Kd*(yaw_err_arr[-1]-yaw_err_arr[-2])*0.1
        print("Yaw Error in degrees: "+str(yaw_err_arr[yaw_len-1]))
    pub.publish(msg)


def ImuCallback(data):
	
	yaw_des = 0
 	#Convert quaternion to euler
	yaw,pitch,roll = quat2euler(data)

	yaw_err = yaw - yaw_des
	yaw_err_arr.append(yaw_err)
	
def quat2euler(data):

    x = data.orientation.x
    y = data.orientation.y
    z = data.orientation.z
    w = data.orientation.w

    yaw_val = math.degrees(math.atan2((2*(x*y+z*w)),(x**2-y**2-z**2+w**2)))
    pitch_val = math.degrees(math.asin((2*(y*z-x*z))))
    roll_val = math.degrees(math.atan2((2*(x*w+y*z)),(x**2+y**2-z**2-w**2)))
    print("Yaw in degrees: "+str(yaw_val))

    return yaw_val,pitch_val,roll_val
########################################
# Main Script
# Initialize our node
rospy.init_node('huskycontrol',anonymous=True)
global yaw_err_arr
yaw_err_arr = []
    
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