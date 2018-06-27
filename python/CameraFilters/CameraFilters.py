#!/usr/bin/python

#                          License Agreement
#                         3-clause BSD License
#
#       Copyright (C) 2018, Xperience.AI, all rights reserved.
#
# Third party copyrights are property of their respective owners.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   * Neither the names of the copyright holders nor the names of the contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# This software is provided by the copyright holders and contributors "as is" and
# any express or implied warranties, including, but not limited to, the implied
# warranties of merchantability and fitness for a particular purpose are disclaimed.
# In no event shall copyright holders or contributors be liable for any direct,
# indirect, incidental, special, exemplary, or consequential damages
# (including, but not limited to, procurement of substitute goods or services;
# loss of use, data, or profits; or business interruption) however caused
# and on any theory of liability, whether in contract, strict liability,
# or tort (including negligence or otherwise) arising in any way out of
# the use of this software, even if advised of the possibility of such damage.

import cv2
import sys
import numpy

PREVIEW = 0
CANNY = 1
BLUR = 2
FEATURES = 3

feature_params = dict( maxCorners = 50,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
s = 0
if len(sys.argv) > 1:
    s = argv[1]

source = cv2.VideoCapture(s)

winName = 'Camera Filters'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
imageFilter = PREVIEW

alive = True
while alive:
    hasFrame, frame = source.read()
    if not hasFrame:
        cv2.waitKey()
        break

    if imageFilter == PREVIEW:
        result = frame;
    elif imageFilter == CANNY:
        result = cv2.Canny(frame, 80, 90);
    elif imageFilter == BLUR:
        result = cv2.blur(frame, (5,5));
    elif imageFilter == FEATURES:
         result = frame
         frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
         if corners is not None:
             for x, y in numpy.float32(corners).reshape(-1, 2):
                 cv2.circle(result, (x,y), 10, (0, 255 , 0), 1)

    cv2.imshow(winName, result)
    key = cv2.waitKey(1)
    if key == 113 or key == 81 or key == 27: # 'Q' || 'q' || Esc
        alive = False
    elif key == 99 or key == 67: # 'C' || 'c'
        imageFilter = CANNY
    elif key == 98 or key == 66: # 'B' || 'b'
        imageFilter = BLUR
    elif key == 102 or key == 70: # 'F' || 'f'
        imageFilter = FEATURES
    elif key == 112 or key == 80: # 'P' || 'p'
        imageFilter = PREVIEW
