from subprocess import call
import threading

def shotsound():
    call(['aplay','shoot.wav'])

def reloadsound():
    call(['aplay','reload.wav'])


def shoot():
    playshot=threading.Thread(target=shotsound)
    playshot.start()

def reload():
    playreload=threading.Thread(target=reloadsound)
    playreload.start()
