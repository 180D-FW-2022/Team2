import cv2 as cv
import bluetooth
import time

# Bluetooth setup
# Replace with bluetooth MAC address of your raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"

# Bluetooth setup
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

'''
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)
'''

while(1):
    #data = client_sock.recv(1024)
    #print("Received:\n" + str(data))
    print("working")
    #cv.imshow('frame', data)

    time.sleep(0.5)

sock.close()