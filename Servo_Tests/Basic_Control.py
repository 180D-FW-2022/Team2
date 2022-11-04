import RPi.GPIO as GPIO
import numpy as np
import time

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin1 = 32
    pin2 = 7
    # Frequency
    freq = 400
    # Duty Cycle
    duty = 60

    GPIO.setwarnings(False)

    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)

    pwm1 = GPIO.PWM(pin1, freq)
    pwm2 = GPIO.PWM(pin2, freq)

    pwm1.start(duty)
    pwm2.start(duty)

    #dutySpread = [54, 57.0, 57.7]

    dutySpread = np.arange(40, 80, 1)

    for duty in dutySpread:
        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        print(duty)
        time.sleep(10)

    pwm1.stop()
    pwm2.stop()

    GPIO.cleanup()