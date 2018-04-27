#!/usr/bin/env python
import requests
import json
from time import sleep
import base64
import rospy
from std_msgs.msg import string
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

bridge = CvBridge()

# Fix this to get an image file as a parameter (subscribe to a Node), and also take in coordinates
def getJSON(data):

    try:
        sign_img_cv2 = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError:
        print("Error: Cannot convert img_msg to cv2")
    else:
        cv2.imwrite('sign_img.jpeg', sign_img_cv2)

    with open("sign_img.jpeg", "rb") as imageFile:
        strtest = base64.b64encode(imageFile.read())
        str2 = strtest.decode("utf-8", "backslashreplace")

    # JSON format expected
    dataSend = {
    "requests": [
    {
    "image": {
    "content": str2
    },
    "features": [
    {
    "type": "TEXT_DETECTION"
    }]}]}

    r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAzgApTEy_zJacjx7EgA6AGTcEfxl9Gako", json = dataSend)
    return dataSend

def talker():
    pub = rospy.Publisher('jsonposter', String, queue_size=50)
    rospy.init_node('poster', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        response = json.dumps(getJSON())
        rospy.loginfo(response)
        pub.publish(response)
        rate.sleep()

def listener():
    rospy.init_node('listener', anonymous=True)
    topic = "/image"
    rospy.Subscriber(topic, Image, getJSON)

if _name_ == '_main_':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass






