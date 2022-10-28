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

    dutySpread = [53.76, 53.78, 53.80, 53.82, 53.84, 54.45, 54.47, 54.49, 54.51, 54.53, 54.55, 56.9, 56.95, 56.98, 57.0, 57.02]

    #dutySpread = np.arange(50, 60, 0.1)

    for duty in dutySpread:
        pwm.ChangeDutyCycle(duty)
        print(duty)
        time.sleep(15)

    pwm.stop()

    GPIO.cleanup()