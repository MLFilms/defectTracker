from darkflow.net.build import TFNet
import cv2
import matplotlib.pyplot as plt
import pprint as pp
import numpy as np
from PIL import Image
import glob
import os
import json

box = 0 # 0 draws a box, 1 plots a point


def standardize(image):
    print(image.dtype)
    image = image.astype(np.float64)
    imgMean = np.mean(image)
    imgSTD = np.std(image)
    image= (image - imgMean)/(6*imgSTD)
    image = image+0.5
    #image = image*255
    image = np.clip(image,0,1)
    return image
    
def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def boxing(original_img , predictions):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
    
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        
        if confidence > 0.3:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            #newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        
    return newImage
    
    
def pointing(original_img , predictions):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
        
        x = int((top_x+btm_x)/2)
        y = int((top_y+btm_y)/2)
    
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        
        if confidence > 0.1:
            newImage = cv2.circle(newImage, (x, y), 2, (255,0,0), -1)
            newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        
    return newImage
	
	
	
	
def processImage(filename, tfnet,box):
    imgcv = cv2.imread(filename)
    #imgcv = rgb2gray(imgcv)
    result = tfnet.return_predict(imgcv)
    #print(result)
    if box ==1:
        newImage = boxing(imgcv, result)
    else:
        newImage = pointing(imgcv, result)
        
    
    im = Image.fromarray(newImage)

    return (im,result)
    #im.save("your_file.jpeg")


options = {"metaLoad": "bin/defectFull.meta", 
           "pbLoad": "bin/defectFull.pb",
           "gpu": 1.0,
		   "threshold": 0.3,
		   "labels": "one_label.txt",
           "json": True
		   }
tfnet = TFNet(options)
targetDir = "E:/Projects/fake/imageData/annotations/corrected"
#'E:/Projects/fake/data/defectData/corrected'
print(targetDir)   
outDir = targetDir+"\\outIMG\\"

if not os.path.exists(outDir):
    os.makedirs(outDir)
'''
xy = []
offPath = os.path.isfile(targetdir+'/offsets.txt')
if exists:
    offsets = np.loadtxt(open(offPath,'rb'))
    offsets = defects.astype(int)
    for line in defects:
        xy.append(line)
        


else:
    xy.append(0)
    xy.append(0)
    # Keep presets   
'''    
filePattern = 	targetDir+"\\*.tif"   

for filename in glob.glob(filePattern):
 
    (im,result) = processImage(filename,tfnet,box)
    sections = filename.split("\\")
    imName = sections[-1]
    im.save(outDir+imName)
    
    numDets = len(result)
    
    for i in range(numDets):
        result[i]['confidence'] = float(result[i]['confidence'])
    
    #print(result)
    dataJSON = json.dumps(result)
    prePost = imName.split(".")
    noEnd = prePost[0]
    
    f = open(outDir+noEnd+".json","w")
    f.write(dataJSON)
    f.close
    
           

#imgcv = cv2.imread("E:\Projects\defectTracker\images\circle_1.jpg")


#print("something")
#wait = input("PRESS ENTER TO CONTINUE.")
#print("something")






