#!/usr/bin/python3
import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((8*10,3), np.float32)
objp[:,:2] = np.mgrid[0:10,0:8].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('/home/zaki/MiniProj_ws/src/myrob/scripts/test.png')

img = cv2.imread(images[0])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, (10, 8), None)

# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)
    corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    imgpoints.append(corners)
    

    # Draw and display the corners
    cv2.drawChessboardCorners(img, (10, 8), corners, ret)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    h,  w = img.shape[:2]
    R, _ = cv2.Rodrigues(rvecs[0])


    homog = np.eye(4)

# Assign rotation matrix to the top-left 3x3 submatrix
    homog[:3, :3] = R

# Assign translation vector to the first three elements of the last column
    
    homog[:3, 3] = np.array(tvecs).flatten()

    print(homog)
    print(mtx)
    cv2.imshow('img',img)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close all windows




