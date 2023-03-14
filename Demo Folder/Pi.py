import bluetooth
from time import sleep
import RPi.GPIO as GPIO
from soundfunctionsfinal import shoot, reload, bluetooth_sound
from lightfunctionsfinal import turnOff, startUp, setHealth, fred
import threading
turnOff()
connected = False
reloaded = True
ammo = 5 #choose a number
ammo1 = ammo
def check():
    global connected
    while(connected==False):
        fred()

def reloading():
    global reloaded
    reload()
    sleep(3)
    reloaded = True
    print("loaded")

#check=threading.Thread(target=check)
#check.daemon = True
#check.start()
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 9000
server_sock.bind(("", port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)
connected = True
#check.join()

startUp()
bluetooth_sound()
sleep(1)
#GPIO.setmode(GPIO.BOARD)

pin_left = 32
pin_right = 33

freq = 400

duty_cw = 35
duty_ccw = 75

GPIO.setwarnings(False)
GPIO.setup(pin_left, GPIO.OUT)
GPIO.setup(pin_right, GPIO.OUT)
pwm_left = GPIO.PWM(pin_left, freq)
pwm_right = GPIO.PWM(pin_right, freq)


while(1):
    data = client_sock.recv(1024)
    print("Received: " + str(data))

    # Sound
    if (str(data).find("y") != -1) and (reloaded == True) and (ammo1 > 0):
        print("Shooting.")
        reloaded = False
        shoot()
        ammo1 = ammo1 - 1
        setHealth((ammo1/ammo)*100)

    if (str(data).find("r") != -1) and (reloaded == False) and (ammo1 > 0):
        print("Reloading.")
        thread = threading.Thread(target=reloading)
        thread.start()
    
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
