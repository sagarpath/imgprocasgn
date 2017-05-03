# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:04:55 2017

@author: shaggy
"""
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

#img = cv2.imread('lena.jpg')
#imga = Image.open('lena.jpg')
#pivot = [100,100]
#scale = 3

img = cv2.imread(sys.argv[1])
# the image path is supplied as the first argument
rows,cols = img.shape[:2]

nrow = range(1,rows)
ncol = range(1,cols)

out = np.zeros( (rows,cols,3), dtype=np.uint8 ) 	#define new blank image that will be filled out as per zoom criterion

print "(Pl note that the image coordinates start from top left corner and right/down in positive)"
pivot1 = input("enter the pivot pixel coordinates: ")
pivot = np.array(pivot1)
scale1 = input("enter the scale: ")
scale = np.float32(scale1) 	#accept pivot point and scale arguments

for i in nrow:
    for j in ncol:
        a = int(pivot[0] - (pivot[0]-i)/scale) 		# determine the pixel in the input image corresponding to a pixel in zoomed image
        b = int(pivot[1] - (pivot[1]-j)/scale)
        if (a<0 or b<0 or a>rows or b>cols):        
            out[i, j] = [0,0,0]            		# if the scale is less than 1 (zooming out) then create black pixels at the pixels not corresponding to any pixels
        else: 
            out[i, j] = img[a, b] 			# copy the signal from pixel corresponding in the input image

#around1 = []						
    #for xi in int(a-1/scale):int(a+1/scale)
	#for yj in int(a-1/scale):int(a+1/scale)
        	#around1.append(img[xi,yj])
    #around = np.array(around1)
#out[i,j] = np.mean(arond)				


# alternatel one can write seperately for scale less than 1 to include an average of multiple pixels in its proximity as in above commented code(downsampling) but its computationally more expensive and this way does not lose much important information such as gradients/edges 
 					
cv2.imwrite("zoomresult.jpg", out)
