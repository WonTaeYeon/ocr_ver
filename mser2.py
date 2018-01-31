import cv2
import numpy as np

img = cv2.imread('handicapSign.jpg')
mser = cv2.MSER_create()

#Resize the image so that MSER can work better
img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
vis = img.copy()

regions = mser.detectRegions(gray)
hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions[0]]
cv2.polylines(vis, hulls, 1, (0,255,0))

mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
for contour in hulls:
    cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

text_only = cv2.bitwise_and(img, img, mask=mask)
print(text_only)


cv2.namedWindow('img', 0)
cv2.imshow('img', vis)
while(cv2.waitKey()!=ord('q')):
    continue
cv2.destroyAllWindows()
