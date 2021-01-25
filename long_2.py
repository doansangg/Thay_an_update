import cv2
import sys
import alphashape
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import numpy as np
from sang import roi
def de_hole(img):
    img=roi(img)[1]
    arr_X=[]
    arr_Y=[]
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    mask = cv2.GaussianBlur(gray,(5,5),0)
    ret1, output = cv2.threshold(mask, 30, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(output,100,200,apertureSize = 3)
    minLineLength = 50
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,2,np.pi/180,15,minLineLength=minLineLength,maxLineGap=maxLineGap)
    if lines is not None:
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                if x1==x2:
                    arr_X.append([x1,y1])
                if y1==y2:
                    arr_Y.append([x1,y1])
        def get_X(box):
            return box[0]
        def get_Y(box):
            return box[1]
        X=sorted(arr_X,key=get_X,reverse=False)
        Y=sorted(arr_Y,key=get_Y,reverse=False)
        x_min,x_max=(X[0]),(X[-1])
        print(x_min)
        (y_min,y_max)=(Y[0],Y[-1])
        img_r=img[y_min[1]:y_max[1],x_min[0]:x_max[0]]
        return ((x_min[0],y_min[1]),img_r)
    else :
        return None
    
def de_hole1(img):
    X_roi,img=de_hole(img)
    arr_X=[]
    arr_Y=[]
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    mask = cv2.GaussianBlur(gray,(5,5),0)
    ret1, output = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(output,100,200,apertureSize = 3)
    minLineLength = 50
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,2,np.pi/180,15,minLineLength=minLineLength,maxLineGap=maxLineGap)
    if lines is not None:
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                if x1==x2:
                    arr_X.append([[x1,y1],[x2,y2]])
                if y1==y2:
                    arr_Y.append([[x1,y1],[x2,y2]])
        def sort_X(box):
            return box[1][1]-box[0][1]
        def sort_Y(box):
            return box[1][0]-box[0][0]
        def get_X(box):
            return box[0][0]
        def get_Y(box):
            return box[1][1]
        X_sort=sorted(arr_X,key=sort_X,reverse=True)
        Y_sort=sorted(arr_Y,key=sort_Y,reverse=True)
        X=sorted(X_sort,key=get_X,reverse=False)
        Y=sorted(Y_sort,key=get_Y,reverse=False)
        X_1=[X_sort[0]]
        for i in X:
            if abs(i[0][0]-X_1[-1][0][0])>10:
                X_1.append(i)
        Y_1=[Y_sort[0]]
        for i in Y:
            if abs(i[1][1]-Y_1[-1][1][1])>10:
                Y_1.append(i)
        X=sorted(X_1,key=get_X,reverse=False)
        Y=sorted(Y_1,key=get_Y,reverse=False)
        Z=[[x[0][0],y[1][1]] for x in X for y in Y]
        X1=[i[0] for i in X]
        for i in X:
            X1.append(i[1])
        Y1=[i[1] for i in Y]
        for i in Y:
            Y1.append(i[0])
        r1=[[img[0]+X_roi[0],img[1]+X_roi[1]] for img in X1]
        r2=[[img[0]+X_roi[0],img[1]+X_roi[1]] for img in Y1]
        r3=[[img[0]+X_roi[0],img[1]+X_roi[1]] for img in Z]
        return (r1,r2,r3)
def get_coor(image):
    X,Y,Z=de_hole1(image)
    Xk=roi(image)[0]
    arr_X=[]
    arr_Y=[]
    for z in Z:
        for x in X:
            if z[0]==x[0] or z[1]==z[1]:
                if check(z,x) :
                    arr_X.append(z)
    for z in Z:
        for x in Y:
            if z[0]==x[0] or z[1]==z[1]:
                if check(z,x) :
                    arr_Y.append(z)
    output=[]
    arr=arr_X+arr_Y
    for x in arr:
        if x not in output:
            output.append(x)
    alpha = 0.3 * alphashape.optimizealpha(output)
    hull = alphashape.alphashape(output, alpha)
    hull_pts = hull.exterior.coords.xy
    arr=[]
    for i in range(len(hull_pts[0])):
        arr.append([int(hull_pts[0][i]),int(hull_pts[1][i])])
    #r1=[[img[0]+Xk[0],img[1]+Xk[1]] for img in arr]
    return arr
def check(coor1,coor2):
    a=abs(coor1[0]-coor2[0])+abs(coor2[1]-coor1[1])
    if a>60:
        return False
    return True
