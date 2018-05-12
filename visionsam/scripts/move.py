#!/usr/bin/env python
from __future__ import print_function, division

import roslib
import sys
import rospy
import tf
import math
import time
from time import sleep
from std_msgs.msg import String
from geometry_msgs.msg import Pose, PoseArray, PoseWithCovarianceStamped, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
    

def main(args):
    rospy.init_node('move', anonymous=True)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goalQueue = [ [2.922, 13.86, 0.0], [11.434, 13.567, 0.0], [19.973, 13.41, 0.0], [26.30, 13.587, 0.0], [22.932, 14.364, 0.0], [12.41, 14.306, 0.0], [5.59, 14.36, 0.0], [6.237, 17.24, 0.0], [6.244, 23.65, 0.0], [6.66, 34.54, 0.0], [5.40, 33.24, 0.0], [5.035, 26.69, 0.0], [5.28, 17.73, 0.0], [5.53, 13.68, 0.0]]


    for g in goalQueue:
        print("Entering goal")
        print(g)
        goal.target_pose.header.frame_id = '/map'
        goal.target_pose.pose.position.x = g[0]
        goal.target_pose.pose.position.y = g[1]
        goal.target_pose.pose.position.z = g[2]
        q = tf.transformations.quaternion_from_euler(0,0,0)
        goal.target_pose.pose.orientation = Quaternion(*q)


        client.send_goal(goal)
        print("Goal sent!")
        wait = client.wait_for_result(rospy.Duration(60))
        print(wait)

        state = client.get_state()
        timer = time.time()
        if (time.time() - timer >= 60):
            print("Timeout")
        print("Goal Completed")


if __name__ == '__main__':
    main(sys.argv)
