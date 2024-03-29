#libraries
import RPi.GPIO as GPIO
from subprocess import call
from time import sleep
#disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO Mode
GPIO.setmode(GPIO.BCM)
#set red,green and blue pins
redPin = [14,27,10,25,0]
greenPin = [15,22,9,8,5]
bluePin = [23,24,11,7,6]
#set pins as outputs
d=0.5
#delay in sleep
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

