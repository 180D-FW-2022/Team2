import cv2 as cv
import bluetooth
import time

# Replace with bluetooth MAC address of your raspberry pi
# For my raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"
# For Gabe's laptop
#bd_addr = "48:D7:05:E7:C7:AA"

# Bluetooth setup
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while(1):
    data = sock.recv(1024)
    print("Received: " + str(data))

    #cv.imshow('frame', data)

    time.sleep(2)

sock.close()