#!/usr/bin/python3
#!/usr/bin/env python3

import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from line_follower_turtlebot.msg import pos

class LineDetect:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/myrob/camera1/image_raw', Image, self.imageCallback)
        self.pub = rospy.Publisher('/pos', pos, queue_size=10)
        self.dir = 1
        self.LowerYellow = np.array([20, 100, 100])
        self.UpperYellow = np.array([30, 255, 255])
        
    def imageCallback(self, data):
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            cv_image = cv2.GaussianBlur(cv_image, (3, 3), 0.1)
            img_hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            img_mask = cv2.inRange(img_hsv, self.LowerYellow, self.UpperYellow)
            height, width, _ = cv_image.shape
            img_mask[0:int(0.8*height), 0:width] = 0
            img_mask[int(0.7*height):height, 0:width] = 0
            M = cv2.moments(img_mask)
            if M["m00"] != 0:
                c_x = int(M["m10"] / M["m00"])
                cv2.circle(img_mask, (c_x, int(height/2)), 5, (155, 200, 0), -1)
                if c_x < width/2-15:
                    self.dir = 0
                elif c_x > width/2+15:
                    self.dir = 2
                else:
                    self.dir = 1
                self.pub.publish(self.dir)
            else:
                self.dir = 3
                self.pub.publish(self.dir)
            cv2.imshow("Robot View", cv_image)
            cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('line_detect')
    ld = LineDetect()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
