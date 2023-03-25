import bluetooth
from time import sleep
import RPi.GPIO as GPIO
from subprocess import call
from soundfunctions import shoot, reload
#from lightfunctions import turnOff, startUp, setHealth

#adding to reset lights
turnOff()
#health variable for demo
health = 100
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

GPIO.setmode(GPIO.BOARD)

pin_left = 32
pin_right = 33
redPin = [14,27,10,25,0]
greenPin = [15,22,9,8,5]
bluePin = [23,24,11,7,6]

d=0.5

for i in range(5):
    GPIO.setup(redPin[i],GPIO.OUT)
    GPIO.setup(greenPin[i],GPIO.OUT)
    GPIO.setup(bluePin[i],GPIO.OUT)

def turnOff():
    for i in range(5):
        GPIO.output(redPin[i],GPIO.LOW)
        GPIO.output(greenPin[i],GPIO.LOW)
        GPIO.output(bluePin[i],GPIO.LOW)
    
def red(i):
    GPIO.output(redPin[i],GPIO.HIGH)
    GPIO.output(greenPin[i],GPIO.LOW)
    GPIO.output(bluePin[i],GPIO.LOW)

def redall():
    for i in range(5):
        GPIO.output(redPin[i],GPIO.HIGH)
        GPIO.output(greenPin[i],GPIO.LOW)
        GPIO.output(bluePin[i],GPIO.LOW)

def green(i):
    GPIO.output(redPin[i],GPIO.LOW)
    GPIO.output(greenPin[i],GPIO.HIGH)
    GPIO.output(bluePin[i],GPIO.LOW)
    
def yellow(i):
    GPIO.output(redPin[i],GPIO.HIGH)
    GPIO.output(greenPin[i],GPIO.HIGH)
    GPIO.output(bluePin[i],GPIO.LOW)
    
def startUp():
    for i in range(5):
        sleep(d)
        green(i)

def setHealth(i):
    if i > 90:
        for j in range(5):
            green(j)
    elif i > 80:
        for j in range(4):
            green(j)
        yellow(4)
    elif i > 70:
        for j in range(4):
            green(j)
        red(4)
    elif i > 60:
        for j in range(3):
            green(j)
        yellow(3)
        red(4)
    elif i > 50:
        redall()
        for j in range(3):
            green(j)
    elif i > 40:
        redall()
        green(0)
        green(1)
        yellow(2)
    elif i > 30:
        redall()
        green(0)
        green(1)
    elif i > 20:
        redall()
        green(0)
        yellow(1)
    elif i > 10:
        redall()
        green(0)
    elif i>0:
        redall()
        yellow(0)
    else:
        redall()

def fred():
    redall()
    sleep(d)
    turnOff()
    sleep(d)
    redall()
    sleep(d)
    turnOff()
    sleep(d)
    redall()
    sleep(d)
    turnOff()

# tried 200
freq_cw = 400
# tried 600
freq_ccw = 800

duty_left = 50
duty_right = 50

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq_cw)
pwm_right = GPIO.PWM(pin_right, freq_cw)

startUp()
setHealth(health)

while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    # Sound
    if str(data).find("y") != -1:
        print("Shooting.")
        shoot()
        health=health-25
        setHealth(health)

    if str(data).find("r") != -1:
        print("Reloading.")
        reload()
    
    # For the left motor
    if str(data).find("q") != -1:
        #print("Moving left motor forward.")
        pwm_left.ChangeFrequency(freq_ccw)
        pwm_left.start(duty_left)
        #pwm_left.ChangeDutyCycle(65)
    elif str(data).find("a") != -1:
        #print("Moving left motor backwards.")
        pwm_left.ChangeFrequency(freq_cw)
        pwm_left.start(duty_left)
        #pwm_left.ChangeDutyCycle(45)


    # For the right motor
    if str(data).find("o") != -1:
        #print("Moving right motor forward.")
        pwm_right.ChangeFrequency(freq_cw)
        pwm_right.start(duty_right)
        #pwm_right.ChangeDutyCycle(45)
    elif str(data).find("l") != -1:
        #print("Moving right motor backwards.")
        pwm_right.ChangeFrequency(freq_ccw)
        pwm_right.start(duty_right)
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
