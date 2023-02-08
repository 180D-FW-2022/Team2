import bluetooth
import time
import RPi.GPIO as GPIO
from soundfunctions import shoot, reload
#from lightfunctions import turnOff, startUp, setHealth

#adding to reset lights
#turnOff()
#health variable for demo
#health = 100
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

duty_cw = 45
duty_ccw = 65

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq)
pwm_right = GPIO.PWM(pin_right, freq)

#startUp()
#setHealth(health)
reloaded = True
while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    # Sound
    if (str(data).find("y") != -1) and (reloaded == True):
        print("Shooting.")
        reloaded = False
        shoot()
        #health=health-25
        #setHealth(health)

    if (str(data).find("r") != -1) and (reloaded == False):
        print("Reloading.")
        reloaded = True
        reload()
    
    # For the left motor
    if str(data).find("q") != -1:
        #print("Moving left motor forward.")
        pwm_left.ChangeFrequency(freq)
        pwm_left.start(duty_cw)
        #pwm_left.ChangeDutyCycle(65)
    elif str(data).find("a") != -1:
        #print("Moving left motor backwards.")
        pwm_left.ChangeFrequency(freq)
        pwm_left.start(duty_ccw)
        #pwm_left.ChangeDutyCycle(45)


    # For the right motor
    if str(data).find("o") != -1:
        #print("Moving right motor forward.")
        pwm_right.ChangeFrequency(freq)
        pwm_right.start(duty_ccw)
        #pwm_right.ChangeDutyCycle(45)
    elif str(data).find("l") != -1:
        #print("Moving right motor backwards.")
        pwm_right.ChangeFrequency(freq)
        pwm_right.start(duty_cw)
        #pwm_right.ChangeDutyCycle(65)
    
    time.sleep(0.1)
    pwm_left.stop()
    pwm_right.stop()
    #pwm_left.ChangeDutyCycle(0)
    #pwm_right.ChangeDutyCycle(0)

#pwm_left.stop()
#pwm_right.stop()
GPIO.cleanup()
client_sock.close()
server_sock.close()
