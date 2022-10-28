import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin = 12;
    # Frequency
    freq = 0.7
    # Duty Cycle
    duty = 50

    # PWM: 12, 13
    # Regular: 22,27,23,24,25,5,6,26

    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, freq)

    pwm.start(duty)

    time.sleep(150)

    pwm.stop()

    GPIO.cleanup()