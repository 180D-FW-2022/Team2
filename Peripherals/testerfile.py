from lightfunctions import turnOff, startUp, setHealth
from time import sleep
from subprocess import call
import threading
def shot():
    call(['aplay','shot.wav'])
playshot=threading.Thread(target=shot)
shot2=threading.Thread(target=shot)
startUp()
sleep(2)
playshot.start()
sleep(0.5)
shot2.start()
playshot=threading.Thread(target=shot)
turnOff()
sleep(5)
j=100
playshot.start()
while j>(-1):
    sleep(0.5)
    setHealth(j)
    j=j-5
sleep(5)
turnOff()
