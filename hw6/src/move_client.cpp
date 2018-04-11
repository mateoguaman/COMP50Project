#include <ros/ros.h>
#include <tf/tf.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_listener.h>
#include <actionlib/server/simple_action_server.h>
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/PoseArray.h"

//typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> Client;

int main(int argc, char ** argv) {
	//Initialize our ROS node
	ros::init (argc, argv, "hw6nav");
	ros::NodeHandle nh;
	
	//create the client object
	actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> nav_client("move_base", true);
	nav_client.waitForServer();
	move_base_msgs::MoveBaseGoal goal;

	//TODO Get Variables
	double targetX0;
	double targetY0;
	double targetZ0;
	double targetX1;
	double targetY1;
	double targetZ1;
	bool flag = 0;
	
	goal.target_pose.header.seq = 1;
	goal.target_pose.header.stamp = ros::Time::now();
	goal.target_pose.header.frame_id = "/map"; //Convention in ROS for robot’s  
 // frame of reference, “/map” for map -> homework

	double initTime = ros::Time::now().toSec();
	bool achievedGoal;
	double timer;		
			
	while (ros::ok()) {
		
		if (!flag) {
			goal.target_pose.pose.position.x = targetX0;
			goal.target_pose.pose.position.y = targetY0;
			goal.target_pose.pose.position.z = targetZ0;
		}	
		else {
			goal.target_pose.pose.position.x = targetX1;
			goal.target_pose.pose.position.y = targetY1;
			goal.target_pose.pose.position.z = targetZ1;
		}
		
		double yaw = 0.0;
		goal.target_pose.pose.orientation = tf::createQuaternionMsgFromYaw(yaw);
	
		//send the goal
		nav_client.sendGoal(goal);

		ros::Rate r(10); //10hz
	
		achievedGoal = nav_client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED;
		timer = ros::Time::now().toSec() - initTime;
		if (achievedGoal && timer <= 60) {
			initTime = ros::Time::now().toSec();
			flag = !flag;
		}
		else {
			nav_client.cancelGoal();
			nav_client.sendGoal(goal);
		}
		ros::spinOnce();
	}

	
}

	//ROS_INFO("Client State: %s\n", client.getState().toString().c_str());
	//nav_client.waitForResult();

