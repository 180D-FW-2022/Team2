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
#tried 400, 300
freq_cw = 200
#tried 500
freq_ccw = 600
# tried 
duty_left = 50
# tried 
duty_right = 50

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq_cw)

pwm_right = GPIO.PWM(pin_right, freq_cw)

while(1):
    data = client_sock.recv(1024)
    #print("Received: " + str(data))

    if str(data) == "b'q'":
        #print("Moving left motor forward.")
        pwm_left.ChangeFrequency(freq_ccw)
        pwm_left.start(duty_left)
    elif str(data) == "b'a'":
        #print("Moving left motor backwards.")
        pwm_left.ChangeFrequency(freq_cw)
        pwm_left.start(duty_left)
    # For the right motor
    elif str(data) == "b'o'":
        #print("Moving right motor forward.")
        pwm_right.ChangeFrequency(freq_cw)
        pwm_right.start(duty_right)
    elif str(data) == "b'l'":
        #print("Moving right motor backwards.")
        pwm_right.ChangeFrequency(freq_ccw)
        pwm_right.start(duty_right)

    time.sleep(0.1)

    pwm_left.stop()
    pwm_right.stop()

GPIO.cleanup()
client_sock.close()
server_sock.close()
