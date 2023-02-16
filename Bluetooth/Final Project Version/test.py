from subprocess import call
import threading
from lightfunctionsfinal import turnOff, redall, fred, startUp
from time import sleep

def shotsound():
    call(['sudo', 'aplay', 'shoot.wav', '-q'])

def reloadsound():
    call(['sudo', 'aplay', 'reload.wav', '-q'])


def shoot():
    playshot=threading.Thread(target=shotsound)
    playshot.start()

def reload():
    playreload=threading.Thread(target=reloadsound)
    playreload.start()

connected = False
def check():
    while(connected==False):
        fred()
turnOff()

check=threading.Thread(target=check)
sleep(4)
print('starting')
check.start()
shoot()
sleep(4)
reload()
sleep(4)
connected = True
check.join()
startUp()
