import cv2 as cv
import numpy as np
import bluetooth
import time

# Replace with bluetooth MAC address of your raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"

# Bluetooth setup
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

# Starting video feed
cap = cv.VideoCapture(0)

# Rescaling video frame
_, frame = cap.read()
scale_percent = 100 # percent of original size
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)

# Initiating midpoint of bounding boxes
midpoint = (0,0)

while(1):
    # Take each frame
    _, frame = cap.read()

    # Resizing frame
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)

    # Creating bounding boxes
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv.boundingRect(c)
        area = cv.contourArea(c)
        if area < 500:
            continue
        x, y, w, h = rect
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        midpoint = (x+(w/2),y+(h/2))

    # Checks to see where midpoint is on the screen
    # Sends out commands based on position
    if midpoint[0] != 0 and midpoint[1] != 0:
        if midpoint[0] < (width/2) :
           if midpoint[1] < (height/2):
               sock.send("q")
           elif midpoint[1] > (height/2):
                sock.send("a")
        elif midpoint[0] > (width/2):
            if midpoint[1] < (height/2):
                sock.send("o")
            elif midpoint[1] > (height/2):
                sock.send("l")
    # Resets midpoint
    midpoint = (0,0)
    
    cv.imshow('frame', frame)

    time.sleep(0.1)

    # Press esc to exit
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

sock.close()
cv.destroyAllWindows()
