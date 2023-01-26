from subprocess import call
import threading

def shotsound():
    call(['aplay','shot.wav'])

def shoot():
    playshot=threading.Thread(target=shotsound)
    playshot.start()
