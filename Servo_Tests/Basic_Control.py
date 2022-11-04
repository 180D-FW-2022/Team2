import RPi.GPIO as GPIO
import numpy as np
import time

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
    GPIO.setup(pin3, GPIO.OUT)

    pwm1 = GPIO.PWM(pin1, freq)
    pwm2 = GPIO.PWM(pin2, freq)
    pwm3 = GPIO.PWM(pin3, freq)

    pwm1.start(duty)
    pwm2.start(duty)
    #pwm3.start(duty)

    #dutySpread = [54, 57.0, 57.7]

    dutySpread = np.arange(68, 75, 0.2)

    duty1 = 60
    duty2 = 69.84
    #69.80000000000003

    for duty in dutySpread:
        pwm1.ChangeDutyCycle(duty1)
        pwm2.ChangeDutyCycle(duty2)
        #pwm3.ChangeDutyCycle(duty)
        print(duty)
        time.sleep(10)

    pwm1.stop()
    pwm2.stop()
    #pwm3.stop()

    GPIO.cleanup()