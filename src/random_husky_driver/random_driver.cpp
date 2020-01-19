#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <stdlib.h>
#include "sensor_msgs/Imu.h"

void chatterCallback(const sensor_msgs::Imu::ConstPtr& msg)
{
  ROS_INFO("Imu Seq: [%d]", msg->header.seq);
  ROS_INFO("Imu Orientation x: [%f], y: [%f], z: [%f], w: [%f]", msg->orientation.x,msg->orientation.y,msg->orientation.z,msg->orientation.w);
}


int main(int argc, char **argv) {
//Initializes ROS, and sets up a node
	ros::init(argc, argv,"random_husky_commands");
	ros::NodeHandle nh;

	ros::init(argc, argv,"imu_listener");
	ros::NodeHandle n;

//Creates the publisher, and tells it to publish to the husky_velocity_controller/cmd_vel topic, with a queue size of 100
	ros::Publisher pub=nh.advertise<geometry_msgs::Twist>("husky_velocity_controller/cmd_vel",100);
/**
   * The subscribe() call is how you tell ROS that you want to receive messages
   * on a given topic.  This invokes a call to the ROS
   * master node, which keeps a registry of who is publishing and who
   * is subscribing.  Messages are passed to a callback function, here
   * called chatterCallback.  subscribe() returns a Subscriber object that you
   * must hold on to until you want to unsubscribe.  When all copies of the Subscriber
   * object go out of scope, this callback will automatically be unsubscribed from
   * this topic.
   *
   * The second parameter to the subscribe() function is the size of the message
   * queue.  If messages are arriving faster than they are being processed, this
   * is the number of messages that will be buffered up before beginning to throw
   * away the oldest ones.
   */
	 ros::Subscriber sub = n.subscribe("/imu/data", 1000, chatterCallback);
//Sets up random number generator
	srand(time(0));

//Sets up loop to publish at a rate of 10Hz
	ros::Rate rate(10);

	while(ros::ok()) {
	//Declares the msg to be sent
		geometry_msgs::Twist msg;

	//Random x value between -2 and 2
    	msg.linear.x=0.4;//*double(rand())/double(RAND_MAX)-2;
    //Random y value between -3 and 3
    	//msg.angular.z=0;//*double(rand())/double(RAND_MAX)-3;
    //Publish the message
    	pub.publish(msg);

    //Delays until its time to send another msg
    	rate.sleep();
	}
}