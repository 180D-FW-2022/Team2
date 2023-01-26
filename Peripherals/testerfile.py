from lightfunctions import turnOff, startUp, setHealth
from soundfunctions import shoot
from time import sleep
<<<<<<< HEAD
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
=======


startUp()
sleep(2)
shoot()
>>>>>>> ee6288cbae7af3b91e3c239008e6ce7024615acb
turnOff()
sleep(5)
j=100
shoot()
while j>(-1):
    sleep(0.5)
    setHealth(j)
    j=j-5
sleep(5)
turnOff()
