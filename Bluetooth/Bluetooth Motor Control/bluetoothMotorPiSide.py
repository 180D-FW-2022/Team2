import bluetooth
import time
import RPi.GPIO as GPIO

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

GPIO.setmode(GPIO.BOARD)

pin = 32
freq = 400

cw = 54
ccw = 58
stop = 0

GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
pwm_left = GPIO.PWM(pin, freq)

while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    if str(data) == "b'q'":
        print("Moving left motor forward.")
        pwm_left.start(cw)
    elif str(data) == "b'a'":
        print("Moving left motor backwards.")
        pwm_left.start(ccw)
    # For the right motor
    #elif str(data) == "o":
    #    pwm.start(cw)
    #elif str(data) == "l":
    #    pwm.start(ccw)

    time.sleep(2)

    pwm_left.stop()

GPIO.cleanup()
client_sock.close()
server_sock.close()
