import cv2 as cv
import numpy as np
import bluetooth
import time
from pocketsphinx import LiveSpeech
import threading

# Bluetooth MAC address of Brian's raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"
# Bluetooth MAC address of Gabe's raspberry pi
#bd_addr = "B8:27:EB:4E:35:33"

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
midpoint_blue = (0,0)
midpoint_green = (0,0)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# define range of green color in HSV
lower_green = np.array([40,40,40])
upper_green = np.array([80,255,255])

# Sound and threading for sound
def recognizeshoot():
    speech = LiveSpeech(keyphrase='shoot', kws_threshold=1e-10)
    for phrase in speech:
        sock.send("y")

def recognizereload():
    speech = LiveSpeech(keyphrase='reload', kws_threshold=1e-20)
    for phrase in speech:
        sock.send("r")

def speech():
    speechshot=threading.Thread(target=recognizeshoot)
    speechreload=threading.Thread(target=recognizereload)
    speechshot.daemon = True
    speechreload.daemon = True
    speechshot.start()
    speechreload.start()

speech()
while(1):
    # Take each frame
    _, frame = cap.read()

    # Resizing frame
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue and red colors
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res_blue = cv.bitwise_and(frame,frame, mask= mask_blue)
    res_green = cv.bitwise_and(frame,frame, mask= mask_green)

    # Creating bounding boxes
    contours_blue, _ = cv.findContours(mask_blue, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for c in contours_blue:
        rect = cv.boundingRect(c)
        area = cv.contourArea(c)
        if area < 500:
            continue
        x, y, w, h = rect
        cv.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        midpoint_blue = (x+(w/2),y+(h/2))

    contours_green, _ = cv.findContours(mask_green, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for c in contours_green:
        rect = cv.boundingRect(c)
        area = cv.contourArea(c)
        if area < 500:
            continue
        x, y, w, h = rect
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        midpoint_green = (x+(w/2),y+(h/2))

    # Checks to see where midpoint is on the screen
    # Updates command based on position
    command = ""
    if midpoint_blue[0] != 0 and midpoint_blue[1] != 0:
        if midpoint_blue[1] < (height/2):
            command += "q"
        elif midpoint_blue[1] > (height/2):
            command += "a"
    if midpoint_green[0] != 0 and midpoint_green[1] != 0:
        if midpoint_green[1] < (height/2):
            command += "o"
        elif midpoint_green[1] > (height/2):
            command += "l"
    sock.send(command)
    # Resets midpoints
    midpoint_blue = (0,0)
    midpoint_green = (0,0)
    
    cv.imshow('frame', frame)

    time.sleep(0.1)

    # Press esc to exit
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

sock.close()
cv.destroyAllWindows()
