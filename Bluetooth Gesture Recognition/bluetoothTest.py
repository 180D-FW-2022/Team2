import bluetooth
import time

bd_addr = "B8:27:EB:0E:7D:93"

port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while(1):
    sock.send("Hello from Surface Laptop!")
    time.sleep(2)

sock.close()