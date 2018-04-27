import cv2
import math
import numpy as np

cap = cv2.VideoCapture('/Users/mateoguaman/Desktop/IMG_1241.MOV')

while(1):
    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
    frameCopy = frame.copy()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Convert BGR to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.uint8(gray)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    #cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cnts = cnts[0]
    #for c in cnts:
    #    M = cv2.moments(c)
    #    peri = cv2.arcLength(c, True)
    #    approx = cv2.approxPolyDP(c, 0.04*peri, True)
    #    if len(approx) == 4:
    #        print('RECTANGLE\n')
    #    c = c.astype("float")
    #    c *= ratio
    #    c = c.astype("int")
    #    cv2.drawContours(frame, [c], -1, (0, 0, 255), 2)
    # define range of blue color in HSV
    lower_blue = np.array([50,50,50])
    upper_blue = np.array([200,255,255])
    lower_green = np.array([40,40,40])
    upper_green = np.array([200,255,255])
    lower_red = np.array([0,0,255])
    upper_red = np.array([150,150, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    maskArray = np.asarray(mask)
    areaSign = np.count_nonzero(maskArray)
    sizeTup = maskArray.shape
    totArea = sizeTup[0] * sizeTup[1]
    ratioWanted = areaSign/totArea
    if ratioWanted > 0.1:
        print(1)
    else:
        print(0)
    dst = cv2.Canny(gray, 100, 200)

    _,contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        print(len(approx))
        if len(approx)==4:
            print("square")
            cv2.drawContours(frameCopy,[cnt],0,(0,0,255),-1)
    maskRect = cv2.inRange(frameCopy, lower_red, upper_red)
    maskRectArray = np.asarray(maskRect)
    res = cv2.bitwise_and(mask, maskRect)

    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(res, kernel, iterations = 1)
    #peri = cv2.arcLength(c, )
    #cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    #cdstP = np.copy(cdst)

    #lines = cv2.HoughLines(dst, 1, np.pi/180, 150)

    #if lines is not None:
    #    for i in range(0, len(lines)):
    #        rho = lines[i][0][0]
    #        theta = lines[i][0][1]
    #        a = math.cos(theta)
    #        b = math.sin(theta)
    #        x0 = a * rho
    #        y0 = b * rho
    #        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    #        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    #        cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    #dst = cv2.cornerHarris(gray, 2, 3, 0.4)
    #dst = cv2.dilate(dst, None)
    #frame[dst > 0.01*dst.max()] = [0, 0, 255]

    #kernel = np.ones((5,5), np.uint8)
    #erosion = cv2.erode(mask, kernel, iterations = 1)
    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    #im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cnt = contours[1]
    #cv2.drawContours(hsv, [cnt], 0, (255,0,0), 3)
    #cv2.drawContours(frame, contours, -1, (255,0,0), 3)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    #res = cv2.bitwise_and(mask, dst);

    cv2.imshow('frame',frame)
    cv2.imshow('frameCopy', frameCopy)
    #cv2.imshow('hsv', hsv)
    cv2.imshow('mask',mask)
    cv2.imshow('maskRect', maskRect)
    cv2.imshow('res', res)
    cv2.imshow('erosion', erosion)
    #cv2.imshow('canny', dst)
    #cv2.imshow('cdst', cdst)
    #cv2.imshow('res',res)
    #cv2.imshow('opening', opening)
    #cv2.imshow('contours', im2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
#tesseract ocr
#abbyy ocr
