import bluetooth
from time import sleep
import RPi.GPIO as GPIO
from soundfunctionsfinal import shoot, reload
from lightfunctionsfinal import turnOff, startUp, setHealth, fred
import threading
turnOff()
connected = False
reloaded = True
def check():
    while(connected==False):
        fred()
        
def reloadtimer():
    sleep(2)
    reload()
    sleep(3)
    reloaded = True

def timerreload():
    timer = threading.Thread(target=reloadtimer)
    timer.start()
    
    
check=threading.Thread(target=check)
check.daemon = True
check.start()

#health variable for demo
health = 100
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)
connected = True
check.join()
startUp()
#GPIO.setmode(GPIO.BOARD)

pin_left = 32
pin_right = 33
# Temporary code for LEDs
#greenPin = [16,15,18,29,31]

freq = 400

duty_cw = 45
duty_ccw = 65

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq_cw)
pwm_right = GPIO.PWM(pin_right, freq_cw)

#setHealth(health)

#light = 0
while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))
    if health == 0:
        break
    # Sound
    if (str(data).find("y") != -1) and (reloaded == True):
        print("Shooting.")
        reloaded = False
        shoot()
        health=health-10
        setHealth(health)
        #health=health-25
        #setHealth(health)

    if (str(data).find("r") != -1) and (reloaded == False):
        print("Reloading.")
        reload()
        reloaded=True
    
    # For the left motor
    if str(data).find("q") != -1:
        #print("Moving left motor forward.")
        pwm_left.ChangeFrequency(freq)
        pwm_left.start(duty_cw)
        #pwm_left.ChangeDutyCycle(65)
    elif str(data).find("a") != -1:
        #print("Moving left motor backwards.")
        pwm_left.ChangeFrequency(freq)
        pwm_left.start(duty_ccw)
        #pwm_left.ChangeDutyCycle(45)


    # For the right motor
    if str(data).find("o") != -1:
        #print("Moving right motor forward.")
        pwm_right.ChangeFrequency(freq)
        pwm_right.start(duty_ccw)
        #pwm_right.ChangeDutyCycle(45)
    elif str(data).find("l") != -1:
        #print("Moving right motor backwards.")
        pwm_right.ChangeFrequency(freq)
        pwm_right.start(duty_cw)
        #pwm_right.ChangeDutyCycle(65)
    
    sleep(0.1)
    pwm_left.stop()
    pwm_right.stop()
    #pwm_left.ChangeDutyCycle(0)
    #pwm_right.ChangeDutyCycle(0)
    
#pwm_left.stop()
#pwm_right.stop()
GPIO.cleanup()
client_sock.close()
server_sock.close()
