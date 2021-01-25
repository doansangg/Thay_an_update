import cv2
import sys
import alphashape
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import numpy as np
from sang import roi
from long_2 import de_hole,check

def de_hole12(img):
    X_roi, img = de_hole(img)
    if de_hole(img) is not None:
        arr_X = []
        arr_Y = []
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = cv2.GaussianBlur(gray, (5, 5), 0)
        ret1, output = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(output, 100, 200, apertureSize=3)
        minLineLength = 50
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges, 2, np.pi / 180, 15, minLineLength=minLineLength, maxLineGap=maxLineGap)
        if lines is not None:
            for x in range(0, len(lines)):
                for x1, y1, x2, y2 in lines[x]:
                    if x1 == x2:
                        arr_X.append([[x1, y1], [x2, y2]])
                    if y1 == y2:
                        arr_Y.append([[x1, y1], [x2, y2]])

            def sort_X(box):
                return box[1][1] - box[0][1]

            def sort_Y(box):
                return box[1][0] - box[0][0]

            def get_X(box):
                return box[0][0]

            def get_Y(box):
                return box[1][1]

            X_sort = sorted(arr_X, key=sort_X, reverse=True)
            Y_sort = sorted(arr_Y, key=sort_Y, reverse=True)
            X = sorted(X_sort, key=get_X, reverse=False)
            Y = sorted(Y_sort, key=get_Y, reverse=False)
            X_1 = [X_sort[0]]
            for i in X:
                if abs(i[0][0] - X_1[-1][0][0]) > 10:
                    X_1.append(i)
            Y_1 = [Y_sort[0]]
            for i in Y:
                if abs(i[1][1] - Y_1[-1][1][1]) > 10:
                    Y_1.append(i)
            X = sorted(X_1, key=get_X, reverse=False)
            Y = sorted(Y_1, key=get_Y, reverse=False)
            Z = [[x[0][0], y[1][1]] for x in X for y in Y]
            X1 = [i[0] for i in X]
            for i in X:
                X1.append(i[1])
            Y1 = [i[1] for i in Y]
            for i in Y:
                Y1.append(i[0])
            r1 = [[img[0] + X_roi[0], img[1] + X_roi[1]] for img in X1]
            r2 = [[img[0] + X_roi[0], img[1] + X_roi[1]] for img in Y1]
            r3 = [[img[0] + X_roi[0], img[1] + X_roi[1]] for img in Z]
            return (r1, r2, r3)
    else:
        return None


def get_coor12(image):
    X, Y, Z = de_hole12(image)
    if de_hole1(image) is not None:
        Xk = roi(image)[0]
        arr_X = []
        arr_Y = []
        for z in Z:
            for x in X:
                if z[0] == x[0] or z[1] == z[1]:
                    if check(z, x):
                        arr_X.append(z)
        for z in Z:
            for x in Y:
                if z[0] == x[0] or z[1] == z[1]:
                    if check(z, x):
                        arr_Y.append(z)
        output = []
        arr = arr_X + arr_Y
        for x in arr:
            if x not in output:
                output.append(x)
        alpha = 0.3 * alphashape.optimizealpha(output)
        hull = alphashape.alphashape(output, alpha)
        hull_pts = hull.exterior.coords.xy
        arr = []
        for i in range(len(hull_pts[0])):
            arr.append([int(hull_pts[0][i]), int(hull_pts[1][i])])

        def check(coor1, coor2):
            a = abs(coor1[0] - coor2[0]) + abs(coor2[1] - coor1[1])
            if a > 10:
                return False
            return True

        hull_pts = hull.exterior.coords.xy
        arr1 = []
        for i in range(len(hull_pts[0])):
            arr1.append([int(hull_pts[0][i]), int(hull_pts[1][i])])
        print(arr1)
        t = {}
        for i in range(len(arr1) - 1):
            t[i] = [arr1[i + 1][0], arr1[i][1]]
        print(t)
        count = 1
        for i in range(len(t)):
            if t[i] is not arr1:
                for v in arr:
                    if check(t[i], v):
                        arr1.insert(count, t[i])
                        count = count + 1
                        print(t[i])
                        break
            count = count + 1
    return arr1