#include <ros/ros.h>
#include <tf/tf.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_listener.h>
#include <actionlib/server/simple_action_server.h>
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/PoseArray.h"

#include <vector>
#include <iostream>


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
    double timer;
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
    ros::init(argc, argv, "move_base_client");
    ros::NodeHandle n;

    //actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> nav_client("move_base",true);
    //nav_client.waitForServer(); //wait to make sure the service is there -- tihs has to be here even if you're use the service is already running
    //move_base_msgs::MoveBaseGoal goal;
  
    double x1 = 0.122;
    double y1 = 0.047;
    double x2 = -4.554;
    double y2 = -0.046;
  
    move_turtle_bot(x1, y1);
    
    while(ros::ok()) {
    
		move_turtle_bot(x2,y2);
		move_turtle_bot(x1,y1);
		
    }
    
  return 0;

}
