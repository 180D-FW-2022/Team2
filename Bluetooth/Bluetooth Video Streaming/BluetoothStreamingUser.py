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
    raw = sock.recv(1024)
    #data = raw.decode('utf-8')
    print("Received:\n" + str(raw))
    #cv.imshow('frame', data)

    time.sleep(0.5)

sock.close()