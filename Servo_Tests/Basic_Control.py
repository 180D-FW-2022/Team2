import RPi.GPIO as GPIO
import numpy as np
import time

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin = 32
    # Frequency
    freq = 400
    # Duty Cycle
    duty = 60

    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, freq)

    pwm.start(duty)

    dutySpread = [53.80000004, 54.5000000006, 57.0, 57.7]

    #dutySpread = np.arange(50, 60, 0.1)

    for duty in dutySpread:
        pwm.ChangeDutyCycle(duty)
        print(duty)
        time.sleep(15)

    pwm.stop()

    GPIO.cleanup()