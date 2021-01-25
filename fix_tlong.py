import cv2
import sys
import numpy as np
import alphashape
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from sang import roi
def get_coor1(img):
    (x1,y1),image=roi(img)
#     cv2.imshow("image",image)
#     cv2.waitKey(0)
    median = cv2.GaussianBlur(image,(5,5),0)
    median = cv2.medianBlur(median,15)
    hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    lower_blue=np.array([91,111,68])
    upper_blue=np.array([115,255,255])
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    edges = cv2.Canny(mask,100,200)
    (contours,_) = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #hull = cv2.convexHull(contours,returnPoints = False)
    #print(hull)
    arr=[]
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        arr.append([x,y])
        arr.append([x+w,y])
        arr.append([x,y+h])
        arr.append([x+w,y+h])
    alpha = 0.4 * alphashape.optimizealpha(arr)
    hull = alphashape.alphashape(arr, alpha)
    if len(hull) > 0:
        hull_pts = hull.exterior.coords.xy
        arr=[]
        for i in range(len(hull_pts[0])):
            arr.append([int(hull_pts[0][i]),int(hull_pts[1][i])])
        #result=[[img[0]+x1,img[1]+y1] for img in arr]
        #results=[(np.array(z)+np.array([x,y])).tolist() for z in arr]
        return arr
    else :
        return arr
