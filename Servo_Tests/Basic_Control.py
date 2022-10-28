import RPi.GPIO as GPIO
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

    for duty in range (40,80):
        pwm.ChangeDutyCycle(duty)
        print(duty)
        time.sleep(5)

    pwm.stop()

    GPIO.cleanup()