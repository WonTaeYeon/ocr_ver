import numpy as np
import cv2

im = cv2.imread('handicapSign.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
print(M)

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

area = cv2.contourArea(cnt)

perimeter = cv2.arcLength(cnt,True)

epsilon = 0.1*cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)

hull = cv2.convexHull(cnt)
k = cv2.isContourConvex(cnt)

x, y, w, h = cv2.boundingRect(cnt)
rect = cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.minAreaRect(cnt)
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(im, [box], 0, (0, 0, 255), 2)

cv2.imshow('test', im)
cv2.waitKey(0)
