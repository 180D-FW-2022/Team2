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

pin_left = 32
pin_right = 33
freq = 400

cw_left = 49
# tried 65
ccw_left = 68
cw_right = 48
ccw_right = 61
stop = 0

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq)
pwm_right = GPIO.PWM(pin_right, freq)

while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    if str(data) == "b'q'":
        print("Moving left motor forward.")
        pwm_left.start(cw_left)
    elif str(data) == "b'a'":
        print("Moving left motor backwards.")
        pwm_left.start(ccw_left)
    # For the right motor
    elif str(data) == "b'o'":
        pwm_right.start(cw_right)
    elif str(data) == "b'l'":
        pwm_right.start(ccw_right)

    time.sleep(0.5)

    pwm_left.stop()
    pwm_right.stop()

GPIO.cleanup()
client_sock.close()
server_sock.close()
