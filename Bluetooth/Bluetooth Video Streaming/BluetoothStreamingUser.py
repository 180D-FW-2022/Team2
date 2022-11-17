import cv2 as cv
import bluetooth
import time

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    #cv.imshow('frame', data)

    time.sleep(2)

client_sock.close()
server_sock.close()
