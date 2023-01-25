import cv2 as cv
import numpy as np
import bluetooth
import time
from io import BytesIO
import sys

# Bluetooth setup
# Replace with bluetooth MAC address of your raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"

# Bluetooth setup
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while(1):
    raw = sock.recv(1048576)
    #data = raw.decode('utf-8')
    print(type(raw))
    print(sys.getsizeof(raw))
    data = BytesIO(raw)
    frame = np.load(data, allow_pickle=True)
    print(type(frame))
    print(frame.size)
    print(frame.shape)

    #print("Received:\n" + str(raw))
    #cv.imshow('frame', data)

    time.sleep(0.5)

sock.close()