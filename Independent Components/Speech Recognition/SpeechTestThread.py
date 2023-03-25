from pocketsphinx import LiveSpeech
import threading
import time
from time import sleep
reference = time.time()

reloaded = True
def recognizeshoot():
    speech = LiveSpeech(keyphrase='shoot', kws_threshold=1e-4)
    for phrase in speech:
        global reloaded
        if reloaded == True:
            print('You said fire: Bombs Away!')
            reloaded = False
        else:
            print('You said fire: You have to reload!')

def recognizereload():
    speech = LiveSpeech(keyphrase='reload', kws_threshold=1e-4)
    for phrase in speech:
        global reloaded
        if reloaded == False:
            print('You said load: Reloading')
            reloading()
        else:
            print('You said load: Already loaded!')

def speech():
    speechshot=threading.Thread(target=recognizeshoot)
    speechreload=threading.Thread(target=recognizereload)
    speechshot.daemon = True
    speechreload.daemon = True
    speechshot.start()
    speechreload.start()

def reloading():
    global reloaded
    sleep(1)
    print('1')
    sleep(1)
    print('2')
    sleep(1)
    reloaded = True
    print('3')
    print('Ready to shoot!')

speech()
print('Searching for keywords, you begin with a loaded cannon')
while True:
    sleep(3)
