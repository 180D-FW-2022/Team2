import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin = 32;
    # Frequency
    freq = 0.7
    # Duty Cycle
    duty = 50

    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, freq)

    pwm.start(duty)

    time.sleep(150)

    pwm.stop()

    GPIO.cleanup()