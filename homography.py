# -*- coding: utf-8 -*-
"""
Created on Wed May  3 13:17:19 2017

@author: shaggy
"""
import sys
import cv
import cv2
import numpy as np
from PIL import Image

#img = cv2.imread('pepsi.jpg')
#imga = Image.open('pepsi.jpg')
#img1_corners = np.float32([[141,276],[503,276],[503,417],[141,417]])
#img2_corners = np.float32([[955,198],[1071,506],[847,504],[717,281]])

img = cv2.imread(sys.argv[1])
# the image path is supplied as the first argument
imga = Image.open(sys.argv[1])
col,row = imga.size

print "(Pl note that the image coordinates start from top left corner and right/down in positive)"
img1corners = input("Enter the corner point coordinates for the original image: ")
img1_corners = np.float32(img1corners)
img2corners = input("Enter the corner point coordinates for the transformed image: ")
img2_corners = np.float32(img2corners)

img1corn = img1_corners

x0 = img1_corners[0,0]
y0 = img1_corners[0,1]

img1corn[:,0] -= x0 		#shifting the origin to top left corner of input image so that the homography matrix and consequently the transformed coordinates do not blow up
img1corn[:,1] -= y0

img2corn = img2_corners

img2corn[:,0] -= x0		#shifting the origin to top left corner of input image so that the homography matrix and consequently the transformed coordinates do not blow up
img2corn[:,1] -= y0

homo1, mask1 = cv2.findHomography(img1corn,img2corn) # calculate homography matrix for this set of points

p=[[0,0,0],[col,0,0],[col,row,0],[row,0,0]]
pp=np.array(p)
tp=np.transpose(pp)
a=homo1.dot(tp) 		# this is to figure out the maximal range of the tranformed image

maxx=a.max(1)
minn=a.min(1)

qmaxw = maxx[1].astype(int)	# allocate this size to the transformed image to safely include all pixels
qmaxh = maxx[0].astype(int)

#print a

if min(img2corn[:,0])<0:
	x_offset = min(img2corn[:,0])
else: 
	x_offset = 0		# calculate negetive offset that might be left out in warpperspective function due to neetive coordinates

#print x_offset

if min(img2corn[:,1])<0:
	y_offset = min(img2corn[:,1])
else: 
	y_offset = 0		# calculate negetive offset that might be left out in warpperspective function due to neetive coordinates

#print y_offset

shunhomo1 = [[ 1 , 0 , -x_offset], [ 0 , 1 , -y_offset], [ 0 , 0 ,    1    ]]
shunhomo = np.array(shunhomo1) 	# define new purely translational homography matrix to compensate for the negetive offset

homo = shunhomo.dot(homo1)	# final homography that will fit the transformed image in minimal positive space

im_dst = cv2.warpPerspective(img, homo,(qmaxw,qmaxh)) 	# final transformed image

cv2.imwrite("homoresult.jpg", im_dst)

