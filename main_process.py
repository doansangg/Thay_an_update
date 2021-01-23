from sorfware import predict
from long_2 import get_coor
from fix_tlong import get_coor1
import argparse
import os
import cv2
import numpy as np
from sang import find_max,find_1,find_2
path_folder1 = "C:/Project/TopicFiles"
from flask import Flask

app = Flask(__name__)


@app.route("/chooseImg/<imageurl>")

path_folder = "../a"
path_weight = "weights/finalized_model_1.sav"
def hello(imageurl):
    img = cv2.imread(os.path.join(path_folder1, imageurl))
    # show(img)

    predict_class = predict(img, path_weight)
    if (predict_class == 1):  # square
        coordinates_result1=get_coor1(img)
        coordinates_result2=get_coor(img)
        resultReturn = ""
        resultReturn = resultReturn + "["
        for i in coordinates_result1:
            resultReturn = resultReturn + '{"x":' + str(i[0]) + ", " + "y"+":"+str(i[1])+ "},"
        resultReturn = resultReturn + "]"
        resultReturn = resultReturn.replace(",]", "]")
        resultReturn1=""
        resultReturn1 = resultReturn1 + "["
        for i in coordinates_result2:
            resultReturn1 = resultReturn1 + '{"x":' + str(i[0]) + ", " + "y"+":"+str(i[1])+ "},"
        resultReturn1 = resultReturn1 + "]"
        resultReturn1 = resultReturn1.replace(",]", "]")
        result=[]
        result.append(resultReturn)
        result.append(resultReturn1)
    	return result
    if (predict_class == 2):  # square
    	resultReturn=""
        resultReturn = resultReturn + "["
        resultReturn = resultReturn + '{"x":' + str(1) + ", " + "y"+":"+str(1)+ "},"
        resultReturn = resultReturn + "]"
        resultReturn = resultReturn.replace(",]", "]")

    	return resultReturn
    if (predict_class == 3):  # square
        coordinates_result1=find_max(img)
        coordinates_result2=find_1(img)
        coordinates_result3=find_2(img)
        resultReturn = ""
        resultReturn = resultReturn + "["
        result=[]
        for k in coordinates_result1:
        	resultReturn = ""
        	resultReturn = resultReturn + "["
        	for i in k:
	            resultReturn = resultReturn + '{"x":' + str(i[0]) + ", " + "y"+":"+str(i[1])+ "},"
	        resultReturn = resultReturn + "]"
        	resultReturn = resultReturn.replace(",]", "]")
        	result.append(resultReturn)
        for k in coordinates_result2:
        	resultReturn = ""
        	resultReturn = resultReturn + "["
        	for i in k:
	            resultReturn = resultReturn + '{"x":' + str(i[0]) + ", " + "y"+":"+str(i[1])+ "},"
	        resultReturn = resultReturn + "]"
        	resultReturn = resultReturn.replace(",]", "]")
        	result.append(resultReturn)
        for k in coordinates_result3:
        	resultReturn = ""
        	resultReturn = resultReturn + "["
        	for i in k:
	            resultReturn = resultReturn + '{"x":' + str(i[0]) + ", " + "y"+":"+str(i[1])+ "},"
	        resultReturn = resultReturn + "]"
        	resultReturn = resultReturn.replace(",]", "]")
        	result.append(resultReturn)
    	return result
    if (predict_class == 4):  # square
    	resultReturn=""
        resultReturn = resultReturn + "["
        resultReturn = resultReturn + '{"x":' + str(1) + ", " + "y"+":"+str(1)+ "},"
        resultReturn = resultReturn + "]"
        resultReturn = resultReturn.replace(",]", "]")

    	return resultReturn
if __name__ == "__main__":
    # main(path_folder)
    app.run(debug=True)
