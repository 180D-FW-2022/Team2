from subprocess import call
import threading

def shotsound():
    call(['sudo', 'aplay', 'shoot.wav', '-q'])

def reloadsound():
    call(['sudo', 'aplay', 'reload.wav', '-q'])

def bluetoothsound():
    call(['sudo', 'aplay', 'bluetooth.wav', '-q'])


def shoot():
    playshot=threading.Thread(target=shotsound)
    playshot.start()

def reload():
    playreload=threading.Thread(target=reloadsound)
    playreload.start()
    
def bluetooth_sound():
    playbluetooth=threading.Thread(target=bluetoothsound)
    playbluetooth.start()
