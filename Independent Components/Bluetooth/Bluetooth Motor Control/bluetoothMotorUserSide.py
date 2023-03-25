import bluetooth
import time
import msvcrt

# Replace with bluetooth MAC address of your raspberry pi
bd_addr = "B8:27:EB:0E:7D:93"

# Bluetooth setup
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

# Control scheme for both left and right motors
print("q = left-forward/na = left-backwards/no = right-forward/nl = right-backwards")

while(1):
    # Grabs user input in real time
    command = msvcrt.getch()
    sock.send(command)

    # Sends every 2 seconds
    time.sleep(0.5)

sock.close()