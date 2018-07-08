#!/usr/bin/python
'''
    OpenCV seamlessCloning Example
    Satya Mallick, LearnOpenCV.com
'''

# Standard imports
import cv2
import numpy as np 

# Read images
dst = cv2.imread("trump.jpg")
src = cv2.imread("obama.jpg")
src_mask = cv2.imread("obama-mask.jpg", cv2.IMREAD_GRAYSCALE)


# Binarize mask
ret, src_mask = cv2.threshold(src_mask, 128,256, cv2.THRESH_BINARY)

# Find the centroid of the mask
m = cv2.moments(src_mask)
center = (int(m['m01']/m['m00']), int(m['m10']/m['m00']) ) 


# Clone seamlessly.
output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)

# Display result
output = np.hstack((dst, src, output))
cv2.imshow("Seamless Cloning", output)
cv2.waitKey(0)



