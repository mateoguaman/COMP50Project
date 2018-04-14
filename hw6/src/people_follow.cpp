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

std::vector<people_msgs::PositionMeasurement> peopleVec;
float currPoseX;
float currPoseY;
float currPoseZ;

float getDistance(float currX, float currY, float targetX, float targetY) {
    return (currX-targetX)*(currX-targetX) + (currY-targetY)*(currY-targetY);
}

void peopleCallback(const people_msgs::PositionMeasurementArray peopleMsg)
{
	peopleVec.clear();
	for (int i = 0; i < peopleMsg.people.size(); i++) {
		peopleVec.push_back(peopleMsg.people[i]);
	}
	ROS_INFO("There are [%lu] people nearby", peopleVec.size());
}

void poseCallback(const geometry_msgs::PoseWithCovarianceStamped poseMsg)
{
    currPoseX = poseMsg.pose.pose.position.x;
    currPoseY = poseMsg.pose.pose.position.y;
    currPoseZ = poseMsg.pose.pose.position.z;
}




bool move_turtle_bot (double x, double y) {
    actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> nav_client("move_base",true);
    nav_client.waitForServer();
    move_base_msgs::MoveBaseGoal goal;
  
	    
    double yaw = 0;
	
    //std::cout<<"Going to :"<< x  << y;
	
    //set the header
    goal.target_pose.header.stamp = ros::Time::now();
    goal.target_pose.header.frame_id = "/map";
	  
    //set relative x, y, and angle
    goal.target_pose.pose.position.x = x;
    goal.target_pose.pose.position.y = y;
    goal.target_pose.pose.position.z = 0.0;
    goal.target_pose.pose.orientation = tf::createQuaternionMsgFromYaw(yaw);

	//send the goal
    nav_client.sendGoal(goal);
    
    bool gotThere = false;
    
    while (!gotThere) {
        if (nav_client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED) {
			gotThere = true;
		}
		else if (nav_client.getState() == actionlib::SimpleClientGoalState::ABORTED) {
			nav_client.cancelGoal();
			break;
		}
	}
    return gotThere;
}




int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");

  ros::NodeHandle n;

  ros::Subscriber peopleSub = n.subscribe("people_tracker_measurements", 10, peopleCallback);

  ros::Subscriber poseSub = n.subscribe("amcl_pose", 100, poseCallback);
  
  while (ros::ok()) {
	int iClosest = -1;
	double minDistance = 1000000;
   
	if (peopleVec.size() > 0) {
		//for (int i = 0; i < peopleVec.size(); i++) {
		//	double dist = getDistance(currPoseX, currPoseY, peopleVec[i].pos.x, peopleVec[i].pos.y);
		//	if (dist < minDistance) {
		//		iClosest = i;
		//		minDistance = dist;
		//	}
		//}
		//ROS_INFO("Found a goal! Going to index [%d] with x: %f and y: %f ", iClosest, currPoseX + peopleVec[iClosest].pos.x, currPoseY + peopleVec[iClosest].pos.y);
		move_turtle_bot(currPoseX + 0.9*peopleVec[0].pos.x, currPoseY + 0.9*peopleVec[0].pos.y);  
	}
	ros::spinOnce();
}


  return 0;
}
