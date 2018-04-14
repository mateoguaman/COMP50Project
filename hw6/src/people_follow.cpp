#include "ros/ros.h"
#include "std_msgs/String.h"
#include <tf/tf.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_listener.h>
#include <actionlib/server/simple_action_server.h>
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/PoseArray.h"
#include "geometry_msgs/PoseWithCovarianceStamped.h"
#include "people_msgs/PositionMeasurementArray.h"
#include "people_msgs/PositionMeasurement.h"
#include <vector>
#include <iostream>


move_base_msgs::MoveBaseGoal goal;
float currPoseX;
float currPoseY;
float currPoseZ;
float scalar = 0.6;
bool haveGoal = false;

void peopleCallback(const people_msgs::PositionMeasurementArray::ConstPtr& peopleMsg)
{
	if (peopleMsg->people.size() > 0) {
		haveGoal = true;
		goal.target_pose.header.stamp = ros::Time::now();
		goal.target_pose.header.frame_id = "/base_link";
		double yaw = 0.0;
		goal.target_pose.pose.position.x =  scalar*(peopleMsg->people[0].pos.x);
    	goal.target_pose.pose.position.y =  scalar*(peopleMsg->people[0].pos.y);
    	goal.target_pose.pose.position.z =  0.00;
    	goal.target_pose.pose.orientation = tf::createQuaternionMsgFromYaw(yaw);    		
	}
}

void poseCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr &poseMsg)
{
}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "people_follow");
	ros::NodeHandle n;
	ros::Subscriber poseSub = n.subscribe("amcl_pose", 1000, poseCallback);
	ros::Subscriber peopleSub = n.subscribe("people_tracker_measurements", 1000, peopleCallback);
	

	actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> nav_client("move_base",true);
	nav_client.waitForServer();
	ros::Rate loop_rate(100);
	double initTime;
	
	while (ros::ok()) {
		ros::spinOnce();

		if (haveGoal) {
			nav_client.sendGoal(goal);
			initTime = ros::Time::now().toSec();
			while (ros::ok()) {
				
				if (ros::Time::now().toSec() - initTime > 15)
				{
					nav_client.cancelGoal();
					break;
				}
				if (nav_client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED) {
					break;
				}
			}
		}
	}
  return 0;
}
