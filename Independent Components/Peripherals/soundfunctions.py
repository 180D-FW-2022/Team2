from subprocess import call
import threading

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
