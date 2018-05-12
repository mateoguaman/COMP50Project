#!/usr/bin/env python
from __future__ import print_function, division

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import tf
import cv2
import math
import time
import numpy as np
import requests
import json
from time import sleep
import base64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, PoseArray, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from cv_bridge import CvBridge, CvBridgeError
import actionlib

class image_converter:
    def __init__(self):
        print("Inside Constructor. Pubs and subs set up")
        self.bridge = CvBridge()
        self.initTime = 0
        self.firstLoop = True
        self.enable = True
        self.signCount = 0
        self.savedFrames = {}
        self.savedFramesStr = ""
        self.currX = None
        self.currY = None
        self.currZ = None
        self.image_sub = rospy.Subscriber("usb_cam/image_raw", Image, self.callbackImage)
        self.pose_sub = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.callbackPose)
        self.json_pub = rospy.Publisher("jsonpub", String, queue_size=10)

    def callbackImage(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            #print("Successful Conversion")
        except CvBridgeError as e:
            print(e)
        frame = cv_image
        frame = cv2.resize(frame,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
        frameCopy = frame.copy()
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40,40,40])
        upper_green = np.array([200,255,255])
        lower_red = np.array([0,0,255])
        upper_red = np.array([150,150, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_green, upper_green)

        contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            #print(len(approx))
            if len(approx)==4:
                #print("square")
                cv2.drawContours(frameCopy,[cnt],0,(0,0,255),-1)
        maskRect = cv2.inRange(frameCopy, lower_red, upper_red)

        kernel = np.ones((5,5), np.uint8)
        erosion = cv2.erode(maskRect, kernel, iterations = 1)
        erosionArray = np.asarray(erosion)
        areaErosion = np.count_nonzero(erosionArray)
        #print("Erosion: %d" % areaErosion)
        sizeTup = erosionArray.shape
        frameArea = sizeTup[0] * sizeTup[1]
        #print("Frame Area: %d" % frameArea)
        ratioWanted  = areaErosion/frameArea
        #print("Ratio of sign is: %d" % ratioWanted)
        if ratioWanted > 0.025:
            print("Detected sign!")
            if self.firstLoop:
                print("Entering firstLoop stuff")
                self.initTime = time.time()
                self.firstLoop = False
                print("Returning")
                return
            elif (self.enable and (time.time() - self.initTime > 0.2)):
                print("Entering processing part!")
                self.enable = False
                self.firstLoop = True
                cv2.imwrite("frame%d.jpeg" % self.signCount, frame)
                with open("frame%d.jpeg" % self.signCount, "rb") as imageFile:
                    img2b64 = base64.b64encode(imageFile.read())
                    encodedImg = img2b64.decode("utf-8", "backslashreplace")
                dataSend = {
                    "requests": [
                        {
                            "image": {
                                "content": encodedImg
                                },
                            "features": [
                                {
                                    "type": "TEXT_DETECTION"
                                }
                            ]
                        }
                    ]
                }
                r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAO9KMCxGvjw9pLQPays74-F8g64EAbDfo", json = dataSend)
                print(time.time())
                if (len(json.loads(r.text).get("responses")[0]) > 0):
                    self.savedFrames['frame%d' % self.signCount] = [time.time(), self.currX, self.currY, json.loads(r.text).get("responses")[0].get("textAnnotations")[0].get("description")]
                    self.signCount += 1
                #self.savedFrames['frame%d' % self.signCount] = [time.time(), self.currX, self.currY, json.loads(r.text).get("responses")[0].get("textAnnotations")[0].get("description")]
                #self.signCount += 1
            #print('Found Sign')
        else:
            #print("Entering else")
            if (time.time() - self.initTime > 0.7):
                self.enable = True
        self.savedFramesStr = json.dumps(self.savedFrames)
        #cv2.imshow('frame',frame)
        #cv2.imshow('frameCopy', frameCopy)
        #cv2.imshow('mask',mask)
        #cv2.imshow('maskRect', maskRect)
        #cv2.imshow('res', res)
        #cv2.imshow('erosion', erosion)
        #k = cv2.waitKey(5) & 0xFF
        #if k == 27:
        #    cv2.destroyAllWindows()
        try:
            self.json_pub.publish(self.savedFramesStr)
        except CvBridgeError as e:
            print(e)

    def callbackPose(self, data):
        self.currX = data.pose.pose.position.x
        self.currY = data.pose.pose.position.y
        self.currZ = data.pose.pose.position.z
        

def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
