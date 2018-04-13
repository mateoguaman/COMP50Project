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
#include <vector>
#include <iostream>

std::vector<people_msgs::PositionMeasurementArray> peopleVec;
float currPoseX;
float currPoseY;
float currPoseZ;

float getDistance(float currX, float currY, float targetX, float targetY) {
    return (currX-targetX)*(currX-targetX) + (currY-targetY)*(currY-targetY);
}

void peopleCallback(const people_msgs::PositionMeasurementArray peopleMsg)
{
  peopleVec = peopleMsg.people;
}

void poseCallback(const geometry_msgs::PoseWithCovarianceStamped poseMsg)
{
    currPoseX = poseMsg.pose.pose.position.x;
    currPoseY = poseMsg.pose.pose.position.y;
    currPoseZ = poseMsg.pose.pose.position.z;
    
    ROS_INFO("Got a pose message with [%f]", poseMsg.pose.pose.position.x);
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
    double initTime = ros::Time::now().toSec();
    
    bool gotThere = false;
    
    while (!gotThere) {
        timer = ros::Time::now().toSec() - initTime;
        if (nav_client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED && timer <= 60) {
            gotThere = true;
        }
        else if (timer > 60)
            nav_client.cancelGoal();
            break;
    } 
    
    return gotThere;
}




int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");

  ros::NodeHandle n;

  ros::Subscriber peopleSub = n.subscribe("people_tracker_measurements", 10, peopleCallback);

  ros::Subscriber poseSub = n.subscribe("amcl_pose", 100, poseCallback);
  
  
  int iClosest = -1;
  double minDistance = 1000000000000;
   
  if (peopleVec.size() > 0) {
    for (int i = 0; i < peopleVec.size(); i++) {
        double dist = getDistance(currPoseX, currPoseY, peopleVec[i].pose.x, peopleVec[i].pose.y)
        if (dist < minDistance) {
            iClosest = i;
            minDistance = dist;
        }
    }
    
    move_turtle_bot(peopleVec[iClosest].pose.x - 0.05, peopleVec[iClosest].pose.y);  
  }
  
  
  ros::spin();


  return 0;
}
