#!/usr/bin/env python
# <!-- <node name="$(anon main)" pkg="clifford_package" type="main4_PD_imu.py" /> -->
import rospy, tf
import geometry_msgs.msg, nav_msgs.msg
from math import *
from time import sleep
from sensor_msgs.msg import Imu
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu

class imu_sensor(object,cargs):
    def __init__(self):
        self.yaw_val = [] # array of first ten yaw values as soon as Clifford boots up
      
    def callback(self,data):
		global yaw_des
		yaw = data.orientation.z
		print "Yaw" +str(yaw)
		if np.size(self.yaw_val) < 10:
			self.yaw_val.append(yaw)
		if np.size(self.yaw_val) > 1:
			Kp = -12
			Kd = 0
			yaw_des = self.yaw_val[1]
			yaw_err = yaw - yaw_des
			print "Yaw (heading) angle error(rad)= " + str(yaw_err)

	
    def controller(yaw): #PD controller for clifford
	    global yaw_des
	    Kp = 70
	    Kd = 7.5
	    yaw_des = self.yaw_val[1]
	    yaw_err = yaw - yaw_des
	    print "Yaw (heading) angle error(rad)= " + str(yaw_err)
	    steer_input = (Kp*yaw_err) + (Kd*0)  
	    return steer_input


    def run(self):
	while not rospy.is_shutdown():
		sub_imu = rospy.Subscriber('/imu/data',Imu,self.callback)
		cmdmsg = geometry_msgs.msg.Twist()
		cmdpub = rospy.Publisher('/cmd_vel',geometry_msgs.msg.Twist, queue_size=10)

	# Setup subscription - which implemets our controller.
	# We pass the publisher, the message to publish and the goal as 
	# additional parameters to the callback function.
		
		rospy.init_node('main4', anonymous=True)
		rospy.spin();


if __name__ == '__main__':
    try:
        node = imu_sensor(cargs)
        node.run()
    except rospy.ROSInterruptException: pass