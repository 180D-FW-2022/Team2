import threading
from pocketsphinx import LiveSpeech
#from soundfunctionsfinal import shoot, reload
#from lightfunctionsfinal import turnOff, startUp, setHealth, fred
from time import sleep
import time

def reloading():
    global reloaded
    sleep(2)
    print("reloadsound")
    sleep(3)
    reloaded = True
    print("loaded")
    
def recognizeshoot():
    global reloaded
    speech = LiveSpeech(keyphrase='shoot', kws_threshold=1e-10)
    for phrase in speech:
        if reloaded == True:
            print("shooting")
            #shoot()
            reloaded = False
        else:
            print("not loaded")

def recognizereload():
    global reloaded
    speech = LiveSpeech(keyphrase='reload', kws_threshold=1e-10)
    for phrase in speech:
        if reloaded == False:
            print("reloading")
            thread = threading.Thread(target=reloading)
            thread.start()
        else:
            print("already loaded")
            
def speech():
    speechshot=threading.Thread(target=recognizeshoot)
    speechreload=threading.Thread(target=recognizereload)
    speechshot.daemon = True
    speechreload.daemon = True
    speechshot.start()
    speechreload.start()
reloaded = True
speech()
Time = time.time()
while(1):
    print(time.time() - Time)
    sleep(1)
