#!/usr/bin/env python

## This script is meant to enable face tracking on a Logitech Orbit MP camera,
## using OpenCV's Haar Cascade Classifier functions.
##
## Max pan/tilt angles of camera (determined with "uvcdynctrl -v -c"):
## 	Tilt = -1920 to 1920
##	Pan  = -4480 to 4480
##
## Author: Andreea Lutac


import cv2 as cv
cv.namedWindow('Camera', cv.WINDOW_AUTOSIZE)

import cv_bridge as cvROS
bridge = cvROS.CvBridge()

import sys
import rospy
import roslib
from sensor_msgs.msg import Image
from rosorbitcamera.msg import Int32Numpy

# Set cascade classifier to use
faceCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/haarcascade_frontalface_default.xml")

def detect_face(msg, args):
	frame = bridge.imgmsg_to_cv2(msg)

	# Run detection
	faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), maxSize=(250, 250), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
	
	bestFace = []
	if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
		bestFace = max(faces, key=lambda item:item[2])
	
	pub=args[0]
	rate=args[1]

	pub.publish(bestFace.tolist() if bestFace != [] else bestFace)
	rate.sleep()


def main():
	nodeID = sys.argv[1]
	rospy.init_node('orbit_face_tracking_n'+str(nodeID), anonymous=True)
	pub = rospy.Publisher('orbit_faces'+str(nodeID), Int32Numpy, queue_size=10)
	rospy.Subscriber('orbit_images', Image, detect_face, callback_args=[pub,rospy.Rate(3)])
	rospy.spin()

if __name__ == '__main__':
	main()
