#!/usr/bin/python3
import rospy
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np

# Define a flag to indicate whether to capture the image or not
capture_image = True
# fc=476.7038
# cc_x=400.5
# cc_y=400.5
# proj_matrix=np.array([[fc,0,cc_x,-33.3692],[0,fc,cc_y,0],[0,0,1,0]])

# camera_mat, rotationMatrix, translationVector, _, _,_,_ = cv2.decomposeProjectionMatrix(proj_matrix)

# print(proj_matrix)
# print(rotationMatrix)
# print(translationVector)


def callback(data):


#     cap = cv2.VideoCapture(2)

#     num = 0

#     while cap.isOpened():

#         succes, img = cap.read()

#         k = cv2.waitKey(5)

#         if k == 27:
#             break
#         elif k == ord('s'): # wait for 's' key to save and exit
#             cv2.imwrite('images/img' + str(num) + '.png', img)
#             print("image saved!")
#             num += 1

#             cv2.imshow('Img',img)

# # Release and destroy all windows before termination
#     cap.release()

#     cv2.destroyAllWindows()
    global capture_image

    if capture_image:
        # Convert the compressed image data to an OpenCV image
        np_arr = np.fromstring(data.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Save the image as "test.png"
        cv2.imwrite("test.png", img)

        # Display the image
        cv2.imshow("Camera Feed", img)
        cv2.waitKey(1)

        # Stop capturing images after the first image is captured
        capture_image = False

        # Close the OpenCV window after capturing the image
        cv2.destroyAllWindows()

# Initialize the ROS node
rospy.init_node('camera_subscriber', anonymous=True)

# Subscribe to the compressed image topic
rospy.Subscriber("/myrob/camera1/image_raw/compressed", CompressedImage, callback)

# Loop to keep the program running until it is interrupted
while not rospy.is_shutdown():
    rospy.spin()