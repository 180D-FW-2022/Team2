import bluetooth
from time import sleep
import RPi.GPIO as GPIO
from soundfunctionsfinal import shoot, reload

#health variable for demo
#health = 100
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

GPIO.setmode(GPIO.BOARD)

pin_left = 32
pin_right = 33
# Temporary code for LEDs
greenPin = [11,15,18,29,36]

freq = 400

duty_cw = 35
duty_ccw = 75

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq)
pwm_right = GPIO.PWM(pin_right, freq)

# Temporary code for LEDs
for i in range(5):
    GPIO.setup(greenPin[i],GPIO.OUT)

# Temporary code for LEDs
d = 0.5
def green(i):
    GPIO.output(greenPin[i],GPIO.HIGH)
def turnOff():
    for i in range(5):
        GPIO.output(greenPin[i],GPIO.LOW)
def startUp():
    for i in range(5):
        sleep(d)
        green(i)


turnOff()
startUp()
reloaded = True
light = 0
while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    # Sound
    if (str(data).find("y") != -1) and (reloaded == True) and (light < 5):
        print("Shooting.")
        reloaded = False
        shoot()
        GPIO.output(greenPin[light],GPIO.LOW)
        light = light + 1

    if (str(data).find("r") != -1) and (reloaded == False) and (light < 5):
        print("Reloading.")
        reload()
        reloaded=True
    
    # For the left motor
    if str(data).find("q") != -1:
        #print("Moving left motor forward.")
        pwm_left.ChangeFrequency(freq)
        pwm_left.start(duty_cw)
    elif str(data).find("a") != -1:
        #print("Moving left motor backwards.")
        pwm_left.ChangeFrequency(freq)
        pwm_left.start(duty_ccw)


    # For the right motor
    if str(data).find("o") != -1:
        #print("Moving right motor forward.")
        pwm_right.ChangeFrequency(freq)
        pwm_right.start(duty_ccw)
    elif str(data).find("l") != -1:
        #print("Moving right motor backwards.")
        pwm_right.ChangeFrequency(freq)
        pwm_right.start(duty_cw)
    
    sleep(0.1)
    pwm_left.stop()
    pwm_right.stop()

GPIO.cleanup()
client_sock.close()
server_sock.close()
