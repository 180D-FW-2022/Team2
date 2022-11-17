import bluetooth
import time

# Replace with bluetooth MAC address of your raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"

# Bluetooth setup
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while(1):
    # This will just send the message below to test bluetooth connectivity
    sock.send("Hello from Surface Laptop!")

    # Sends every 2 seconds
    time.sleep(2)

sock.close()