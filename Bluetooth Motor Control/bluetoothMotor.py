import bluetooth
import time
import msvcrt

bd_addr = "B8:27:EB:0E:7D:93"

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

print("q = left-forward/na = left-backwards/no = right-forward/nl = right-backwards")

while(1):
    command = msvcrt.getch()
    sock.send(command)
    time.sleep(2)

sock.close()