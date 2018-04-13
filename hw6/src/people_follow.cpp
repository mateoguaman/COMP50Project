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

void peopleCallback(const people_msgs::PositionMeasurementArray peopleMsg)
{
  ROS_INFO("Got [%lu] people in the frame", peopleMsg.people.size());
}

void poseCallback(const geometry_msgs::PoseWithCovarianceStamped poseMsg)
{
    ROS_INFO("Got a pose message with [%f]", poseMsg.pose.pose.position.x);
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");

  ros::NodeHandle n;

  ros::Subscriber peopleSub = n.subscribe("people_tracker_measurements", 10, peopleCallback);

  ros::Subscriber poseSub = n.subscribe("amcl_pose", 100, poseCallback);
  
  ros::spin();


  return 0;
}
