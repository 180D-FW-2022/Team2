import cv2 as cv
import numpy as np
import time
from io import BytesIO

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

    '''
    print(frame)
    print(frame.size)
    print(frame.shape)
    print(frame.dtype)
    print(type(frame))
    '''

    np_bytes= BytesIO()
    np.save(np_bytes, frame, allow_pickle=True)

    np_bytes = np_bytes.getvalue()
    print(type(np_bytes))

    decode = BytesIO(np_bytes)
    decoded = np.load(decode, allow_pickle=True)
    print(decoded)

    if np.array_equal(frame, decoded):
        print("true")
    else:
        print("false")

    time.sleep(2)

    # Press esc to exit
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()