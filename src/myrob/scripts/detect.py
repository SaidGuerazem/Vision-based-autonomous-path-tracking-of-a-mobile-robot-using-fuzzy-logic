#!/usr/bin/python3

import rospy 
import cv2
import numpy as np 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge
import glob
import matplotlib.pyplot as plt
import math
from myrob.msg import error
from myrob.msg import bend


fc=476.7038
cc_x=400.5
cc_y=400.5

T1 = np.array([[1, -0.0026, 0.0037, -0.1147482],
                [0.0045, 0.6405 , -0.7680, -0.065923],
                [-0.0004, 0.7680, 0.6405, 0.4089230],
                [0,           0,       0,         1]])
T2 = np.array([[0, -1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1]])

transformation_matrix = np.dot(T1, T2)

 
camera_matrix = np.array([[487.19, 0, 0],
                          [0, 430.197,0],
                          [400.9021, 341.0977, 1]])
 
230

t = transformation_matrix[:3,3]
R = transformation_matrix[:3,:3]

R_inv = np.linalg.inv(R)
A_inv = np.linalg.inv(camera_matrix)

def pixel_to_world(u, v, t = t, R_inv = R_inv, A_inv = A_inv):
    p = np.array([u, v, 1])
    p_1=np.dot(p, A_inv) - t
    p_1=np.dot(p_1, R_inv)
    return p_1

in_between=0

def process(image):
    global error_1
    global error_2
    global bend_norm
    global in_between

    alpha= 1




    bridge=CvBridge()


    

    cv_image=bridge.imgmsg_to_cv2(image,"bgr8")

    hsv_image=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)

    h, w, _ = cv_image.shape
    num_masks = 15

# Calculate the height interval between each mask
    interval = int(0.8 * h) // (num_masks - 1)

# Initialize the starting height
    start_height = int(0.2* h)

# Initialize the masks list
    masks = []

# Loop to create and configure the additional masks
    for i in range(num_masks):
        mask = cv2.inRange(hsv_image, (20, 50, 50), (60, 255, 255))

    # Set the mask regions
        mask[0:start_height, 0:w] = 0
        mask[start_height + int(0.05 * h):h, 0:w] = 0

    # Append the mask to the list
        masks.append(mask)

    # Show the mask
       

    # Update the starting height for the next mask
        start_height += interval


    
    centroids = []

    for mask in masks:
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            centroids.append((cx, cy))
            cv2.circle(mask, (cx, cy), 5, (155, 200, 0), -1)

    


    centroids_homog = []
    x_coords = [coord[0] for coord in centroids]
    y_coords = [coord[1] for coord in centroids]
    x_coords = x_coords[::-1]
    for cx, cy in zip(x_coords, y_coords):
        centroids_homog.append(pixel_to_world(cx, cy))
# Convert pixel coordinates to ground plane coordinates
    centroids_ground = centroids_homog
    

    p_ref_1 = pixel_to_world(w/2, min(y_coords))
    p_ref_2 = pixel_to_world(h/2, max(y_coords))

    x_coords = np.array([coord[0] for coord in centroids_ground])*(-1)
    y_coords = np.array([coord[1] for coord in centroids_ground])*(-1)

 
    x_ref_1 = p_ref_1[0]*(-1)
    x_ref_2 = p_ref_2[0]*(-1)

    y_ref_1 = p_ref_1[1]*(-1)
    y_ref_2 = p_ref_2[1]*(-1)
    x_coords = x_coords
    y_coords = y_coords
    x_ref = np.array([x_ref_1, x_ref_2])
    y_ref = np.array([y_ref_1, y_ref_2])
 
    
# Fit a cubic polynomial through the points to estimate parameters  
    curve = np.polyfit(x_coords, y_coords, 3)

    curvature = np.abs(6*curve[3]*x_ref_2 + 2*curve[2]) / np.abs((1 + (3*curve[3]*(x_ref_2)**2 + 2*curve[2]*x_ref_2 +curve[1])**2)**1.5)

    curvature = 1/curvature
    bend_norm = curvature

    y_2_hat = (curve[3]*(x_ref_2)**3 + curve[2]*(x_ref_2)**2+  curve[1]*(x_ref_2) + curve[0]) 

    lateral_error = y_2_hat - y_ref_2

    # heading_error = 3*curve[3]*(x_ref_2)**2 + 2*curve[2]*x_ref_2 + curve[1]
    L = np.linalg.norm(np.array([x_ref_1 - x_ref_2, y_ref_1 - y_ref_2]))



    print('visualisation distance: ', L)

    heading_error = math.atan(lateral_error/L)


    error_1=alpha*lateral_error+(1-alpha)*heading_error
    error_2=error_1-in_between
    
    in_between=error_1

#     x_plot = np.linspace(min(x_coords),  max(x_coords), 100)

#     print('curvature', curvature)
#     print('e_l',lateral_error)
#     print('e_phi',heading_error)

# # Evaluate the polynomial at the x values
#     y_plot = np.polyval(curve, x_plot)

# # Plot the original points and the polynomial curve
#     plt.scatter(x_coords, y_coords, color='blue', label='Data Points')
#     plt.plot(x_ref, y_ref)
#     plt.plot(x_plot, y_plot, color='red', label='Polynomial Curve')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


def main() :

    global error_1
    global error_2
    global bend_norm
   

    rospy.init_node("image_processeur")

  

    rospy.Subscriber("/myrob/camera1/image_raw",Image,process)
    rospy.sleep(2)
    pub1=rospy.Publisher("/error",error,queue_size=10)
    pub2=rospy.Publisher("/bend",bend,queue_size=10)

    rate=rospy.Rate(10)

    while not rospy.is_shutdown():
        error.e1=error_1
        error.e2=error_2
        bend.c_norm=bend_norm
        pub1.publish(error)
        pub2.publish(error)

        rate.sleep()
   

main()
