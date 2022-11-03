import RPi.GPIO as GPIO
import numpy as np
import time

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin = 32
    # Frequency
    freq = 400
    # Duty Cycle: 54 CW, 58 CCW, 0 for stopped. Works for both servos
    duty = 54

    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, freq)

    pwm.start(duty)

    #Set how long you wish to run in seconds (can add while(True) loop for indefinite)
    time.sleep(100)

    pwm.stop()

    GPIO.cleanup()