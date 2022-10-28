import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    # PWM Pin
    pin = 32
    # Frequency
    freq = 1000
    # Duty Cycle
    duty = 100

    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, freq)

    pwm.start(duty)

    #pwm.ChangeDutyCycle(duty)

    time.sleep(150)

    pwm.stop()

    GPIO.cleanup()