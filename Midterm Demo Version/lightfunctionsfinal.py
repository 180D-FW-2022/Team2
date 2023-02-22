import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#set red,green pins, not using blue
greenPin = [11,15,18,29,36]
redPin = [13,16,22,31,37]

#set pins as outputs
d=0.5
#delay in sleep
for i in range(5):
    GPIO.setup(redPin[i],GPIO.OUT)
    GPIO.setup(greenPin[i],GPIO.OUT)


def turnOff():
    for i in range(5):
        GPIO.output(redPin[i],GPIO.LOW)
        GPIO.output(greenPin[i],GPIO.LOW)

    
def red(i):
    GPIO.output(redPin[i],GPIO.HIGH)
    GPIO.output(greenPin[i],GPIO.LOW)


def redall():
    for i in range(5):
        GPIO.output(redPin[i],GPIO.HIGH)
        GPIO.output(greenPin[i],GPIO.LOW)


def green(i):
    GPIO.output(redPin[i],GPIO.LOW)
    GPIO.output(greenPin[i],GPIO.HIGH)

    
def yellow(i):
    GPIO.output(redPin[i],GPIO.HIGH)
    GPIO.output(greenPin[i],GPIO.HIGH)

    
def startUp():
    turnOff()
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
