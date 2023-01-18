#libraries
import RPi.GPIO as GPIO
import os
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
    
def fred():
    redall()
    sleep(.5)
    turnOff()
    sleep(.5)
    redall()
    sleep(.5)
    turnOff()
    sleep(.5)
    redall()
    sleep(.5)
    turnOff()
   
green(0)
green(1)
yellow(2)
red(3)
red(4)
sleep(2)
turnOff()
