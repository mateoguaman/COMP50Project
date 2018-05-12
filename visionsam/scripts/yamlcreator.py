#!/usr/bin/env python
from __future__ import print_function, division

import roslib
import json
import rospy
from std_msgs.msg import String

def parseInput(data_str):
    obj = json.loads(data_str)
    return obj

def get_description(label):
    # check if label is empty
    if not label:
        print("Error: Label not found")
        return False, ""

    # If it is a room number check if 3 digit number. If not discard it
    if label[0].isdigit:
        if len(label) < 3:
            return False, ""
        if not label[1].isdigit:
            return False, ""
        if not label[2].isdigit:
            return False, ""

        if len(label) > 3 and label[3].isdigit:
            if label[3] == '8':
                label_list = list(label)
                label_list[3] = 'B'
                label = "".join(label_list)

    # replace all new lines with a space.
    label = label.replace('\n', ' ')

    if len(label) <= 3:
        return False, ""

    return True, label

def write_to_yaml(data_str):
    radius = 0.5  #  Choose appropriate radius
    z = 0  		  #  z-position
    
    if (len(data_str) == 2):
	return

    data = parseInput(data_str)
    num_frames = len(data)

    file = open("sam.yaml", "w")

    for i in range(0, num_frames):
        frame = "frame" + str(i)
        x = data[frame][1]
        y = data[frame][2]
        flag, label = get_description(data[frame][3])

        if flag:
            file.write("name: " + label)
            file.write("\nframe_id: map\n")
            file.write("radius: " + str(radius))
            file.write("\npose: \n")
            file.write("\tposition:\n\t\tx: " + str(x) + "\n\t\ty: " + str(y) + "\n\t\tz: " + str(z) + "\n")
            file.write("\torientation:\n\t\tx: 0\n\t\ty: 0\n\t\tz: 0\n\t\tw: 1\n\n")

    file.close()

def callback(data_str):
    #print("Entering callback")
    write_to_yaml(data_str.data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("jsonpub", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
