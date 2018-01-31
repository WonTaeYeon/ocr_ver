from PIL import Image
import numpy as np
import cv2

## Read image and change the color space
imgname = "test_4.jpg"
img = cv2.imread(imgname)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

## Get mser, and set parameters
mser = cv2.MSER_create()
mser.setMinArea(0)
mser.setMaxArea(10000)

## Do mser detection, get the coodinates and bboxes
coordinates, bboxes = mser.detectRegions(gray)

## Filter the coordinates
vis = img.copy()
boxs = []
coords = []


def resize(num):
    a = 1
    while len(boxs)-num > a:
        x1 = boxs[num][0] + boxs[num][2]
        x2 = boxs[num + 1][0]
        x3 = x2 + boxs[num + 1][2]
        y1 = boxs[num][1] + boxs[num][3]
        y2 = boxs[num + 1][1]
        y3 = y2 + boxs[num + 1][3]
        if x1 >= x2 >= boxs[num][0] or y1 >= y2 >= boxs[num][1]:
            if x1 >= x2:
                if x1 < x3:
                    boxs[num][2] += x3 - x1
                    print('ok1')
            if y1 >= y2:
                if y1 < y3:
                    boxs[num][3] += y3 - y1
                    print('ok2')
            del boxs[num + 1]
        else:
            break
        print("a", a)
        a += 1


for coord in coordinates:
    bbox = cv2.boundingRect(coord)
    x, y, w, h = bbox
    # cv2.rectangle(gray, (x-2, y-2), (x+w+2, y+h+2),(3, 255, 4), 1)
    coords.append(coord)
    boxs.append([x, y, w, h])


for i in range(len(boxs)):
    if i == len(boxs)-2:
        break
    else:
        print(i)
        resize(i)
        continue

for i in range(len(boxs)):
    print(boxs[i])
    x = boxs[i][0]
    y = boxs[i][1]
    w = boxs[i][2]
    h = boxs[i][3]
    cv2.rectangle(gray, (x , y), (x + w, y + h), (3, 255, 4), 1)
cv2.imshow("hi", gray)
cv2.waitKey(0)

## colors
# colors = [[255,255,255]]
colors = [[43, 43, 200], [43, 75, 200], [43, 106, 200], [43, 137, 200], [43, 169, 200], [43, 200, 195], [43, 200, 163],
          [43, 200, 132], [43, 200, 101], [43, 200, 69], [54, 200, 43], [85, 200, 43], [116, 200, 43], [148, 200, 43],
          [179, 200, 43], [200, 184, 43], [200, 153, 43], [200, 122, 43], [200, 90, 43], [200, 59, 43], [200, 43, 64],
          [200, 43, 95], [200, 43, 127], [200, 43, 158], [200, 43, 190], [174, 43, 200], [142, 43, 200], [111, 43, 200],
          [80, 43, 200], [43, 43, 200]]

## Fill with random colors
np.random.seed(0)
canvas1 = img.copy()
canvas2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
canvas3 = np.zeros_like(img)

for cnt in coords:
    xx = cnt[:, 0]
    yy = cnt[:, 1]
    color = colors[np.random.choice(len(colors))]
    canvas1[yy, xx] = color
    canvas2[yy, xx] = color
    canvas3[yy, xx] = color

## Save
cv2.imwrite("result1.png", canvas1)
cv2.imwrite("result2.png", canvas2)
cv2.imwrite("result3.png", canvas3)

# cv2.imshow("imgae_1", canvas3)
# cv2.waitKey(0)

# for coord in coordinates:
#     bbox = cv2.boundingRect(coord)
#     x, y, w, h = bbox
#     cv2.rectangle(canvas1, (x - 2, y - 2), (x + w + 2, y + h + 2), (3, 255, 4), 1)

# cv2.imshow("canvas3", canvas1)
# cv2.waitKey(0)


