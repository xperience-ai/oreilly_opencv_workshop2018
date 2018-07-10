'''
Panorama using OpenCV

Satya Mallick, LearnOpenCV.com 
'''

import sys
import cv2
import glob

if __name__ == "__main__":

	print("USAGE : panorama.py <path to folder containing images>")

	# Read the images from directory
	dir_name = "boat"
	if sys.argv[1]:
		dir_name = sys.argv[1].rstrip("/")

	imagefiles = glob.glob("{}/*".format(dir_name))
	imagefiles.sort()

	images = []
	for filename in imagefiles:
		img = cv2.imread(filename)
		images.append(img)

	# Default output file path
	output_file = "{}_result.png".format(dir_name) 
	
	# create stitcher object using stitcher class
	stitcher = cv2.createStitcher()

	status, result = stitcher.stitch(images)

	# Write output to disk
	if status == 0:
		cv2.imwrite(output_file, result)
		print("Output image written to {}".format(output_file))
	else:
		print("Error in Stitching, Error Code : {}".format(status))
