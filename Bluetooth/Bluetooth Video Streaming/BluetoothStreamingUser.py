import cv2 as cv
import bluetooth
import time

# Bluetooth setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

while(1):
    data = sock.recv(1024)
    print("Received:\n" + str(data))
    
    #cv.imshow('frame', data)

    time.sleep(0.5)

client_sock.close()
server_sock.close()