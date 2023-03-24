from lightfunctions import turnOff, startUp, setHealth
from soundfunctions import shoot
from time import sleep
turnOff()
startUp()
sleep(2)
shoot()
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
