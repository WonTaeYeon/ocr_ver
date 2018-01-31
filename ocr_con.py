import cv2
import numpy as np
import random
import pytesseract
from PIL import Image

def roi(img, minX,minY,maxX,maxY, color3=(255, 255, 255), color1=255):
    vertices = np.array([[(minX-3, minY-3), (minX-3, maxY+3),
                          (maxX+3, maxY+3), (maxX+3, minY-3)]], dtype=np.int32)
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        color = color3
    else:
        color = color1
    cv2.fillPoly(mask, vertices, color)
    roiImg = cv2.bitwise_and(img, mask)
    return roiImg

def preProcessing(img):
    origin = cv2.imread(img)
    #origin = cv2.resize(origin, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
    #cv2.imshow('Origin',origin)

    grayScale = cv2.cvtColor(origin, cv2.COLOR_RGB2GRAY)
    #cv2.imshow('gray',grayScale)

    canny = cv2.Canny(grayScale, 70,90)
    #cv2.imshow('Canny',canny)

    e= cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    img = cv2.dilate(canny,e, iterations=1)
    #cv2.imshow('Dilate',img)

    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(img, contours,-1,(255,255,255),2)
    #cv2.imshow('Contours',img)


    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #roi
    roiImgs=[]
    for j,i in enumerate(range(len(contours))):
        r = random.randrange(1,255)
        g = random.randrange(1,255)
        b = random.randrange(1,255)
        cnt = contours[i]
        cnt=np.squeeze(cnt)
        xs=[]
        ys=[]
        for x,y in cnt:
            xs.append(x)
            ys.append(y)
        maxX,maxY,minX,minY = max(xs),max(ys),min(xs),min(ys)
        if maxX-minX<15 and maxY-minY<12:
            pass
        else:
            roiImg=roi(grayScale,minX,minY,maxX,maxY)
            roiImgs.append(roiImg)
            if j<3:
                #cv2.imshow(str(j), roiImg)
                pass
            result = cv2.rectangle(origin,(minX-3,minY-3),(maxX+3,maxY+3),(b,g,r),1)
            #result = cv2.drawContours(origin,[cnt],-1,(b,g,r),2)

    cv2.imshow('hierachy',result)
    cv2.imwrite('rec_result.jpg', result)

    return roiImgs

'''--------------------main-------------------'''
roiImgs=preProcessing('capture.JPG')
pytesseract.pytesseract.tesseract_cmd = 'C:/Tesseract-OCR/tesseract'


cv2.imshow("sample", roiImgs[24])
cv2.imwrite('sample.jpg', roiImgs[24])
print(pytesseract.image_to_string(roiImgs[24], lang='eng'))

cv2.waitKey(0)
cv2.destroyAllWindows()