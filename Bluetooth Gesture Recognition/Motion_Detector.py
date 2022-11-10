import cv2 as cv
import numpy as np
import bluetooth
import time

bd_addr = "B8:27:EB:0E:7D:93"

port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

cap = cv.VideoCapture(0)

while(1):
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)

    #cv.imshow('frame',frame)
    #cv.imshow('mask',mask)
    #cv.imshow('res',res)

    # Creating bounding boxes
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv.boundingRect(c)
        area = cv.contourArea(c)
        if area < 500:
            continue
        x, y, w, h = rect
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

    cv.imshow('frame', frame)

    # Press esc to exit
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
