#libraries
import RPi.GPIO as GPIO
import os
from time import sleep
#disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO Mode
GPIO.setmode(GPIO.BCM)
#set red,green and blue pins
redPin = 12
greenPin = 6
bluePin = 13
#set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

def turnOff():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)
    
def red():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)

def green():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.LOW)
    
def yellow():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.LOW)
    
def fred():
    red()
    sleep(.5)
    turnOff()
    sleep(.5)
    red()
    sleep(.5)
    turnOff()
    sleep(.5)
    red()
    sleep(.5)
    turnOff()
    
def fyellow():
    yellow()
    sleep(.5)
    turnOff()
    sleep(.5)
    yellow()
    sleep(.5)
    turnOff()
    sleep(.5)
    yellow()
    sleep(.5)
    turnOff()

def fgreen():
    green()
    sleep(.5)
    turnOff()
    sleep(.5)
    green()
    sleep(.5)
    turnOff()
    sleep(.5)
    green()
    sleep(.5)
    turnOff()
