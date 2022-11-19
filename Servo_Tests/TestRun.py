import RPi.GPIO as GPIO
import numpy as np
import time

#Pin 1: 32 is LS
#Pin 2: 33 is RS
#Pin 3: 37 is TS


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin1 = 32
    pin2 = 33
    pin3 = 37
    # Frequency
    freq = 400
    # Duty Cycle
    duty = 60

    GPIO.setwarnings(False)

    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    #GPIO.setup(pin3, GPIO.OUT)

    pwm1 = GPIO.PWM(pin1, freq)
    pwm2 = GPIO.PWM(pin2, freq)
    #pwm3 = GPIO.PWM(pin3, freq)

    pwm1.start(0)
    pwm2.start(0)
    print("Hold on to your butts!")
    time.sleep(3)

    pwm1.ChangeDutyCycle(41.5)
    pwm2.ChangeDutyCycle(69.82)
    print("Forward")
    time.sleep(10)

    pwm1.ChangeDutyCycle(60)
    pwm2.ChangeDutyCycle(51)
    print("Backward")
    time.sleep(8)

    pwm1.ChangeDutyCycle(65)
    pwm2.ChangeDutyCycle(61)
    print("Left")
    time.sleep(2)

    pwm1.ChangeDutyCycle(49)
    pwm2.ChangeDutyCycle(48)
    print("Right")
    time.sleep(2)

    pwm1.ChangeDutyCycle(65)
    pwm2.ChangeDutyCycle(61)
    print("Left")
    time.sleep(4)

    pwm1.ChangeDutyCycle(60)
    pwm2.ChangeDutyCycle(51)
    print("Backward")
    time.sleep(7)

    pwm1.ChangeDutyCycle(49)
    pwm2.ChangeDutyCycle(48)
    print("Right")
    time.sleep(4)

    pwm1.ChangeDutyCycle(41.5)
    pwm2.ChangeDutyCycle(69.82)
    print("Forward")
    time.sleep(8)

    pwm1.stop()
    pwm2.stop()
    #pwm3.stop()

    GPIO.cleanup()