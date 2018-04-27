import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('/Users/mateoguaman/Desktop/IMG_0824.JPG')
#img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
lower_green = np.array([50, 50, 50])
upper_green = np.array([200,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green)
maskArray = np.asarray(mask)
area = np.count_nonzero(maskArray)
print("Dimensions")
sizeTup = maskArray.shape
print(sizeTup)
totArea = sizeTup[0] * sizeTup[1]
print(totArea)
print(area)
ratioWanted = area/totArea
print(ratioWanted)

res = cv2.bitwise_and(img,img, mask= mask)

ret,thresh = cv2.threshold(gray,127,255,1)

_,contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print(len(approx))
    if len(approx)==4:
        print("square")
        cv2.drawContours(img,[cnt],0,(0,0,255),-1)

#print(mask)
cv2.imshow('image', img)
cv2.imshow('mask', mask)
cv2.imshow('res', res)
while(1):
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
