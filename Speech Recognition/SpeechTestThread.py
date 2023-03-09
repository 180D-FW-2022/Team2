from pocketsphinx import LiveSpeech
import threading
import time
from time import sleep
reference = time.time()
def recognizeshoot():
    speech = LiveSpeech(keyphrase='shoot', kws_threshold=1e-4)
    for phrase in speech:
        print('shooting')

def recognizereload():
    speech = LiveSpeech(keyphrase='reload', kws_threshold=1e-4)
    for phrase in speech:
        print('reloading')

def speech():
    speechshot=threading.Thread(target=recognizeshoot)
    speechreload=threading.Thread(target=recognizereload)
    speechshot.daemon = True
    speechreload.daemon = True
    speechshot.start()
    speechreload.start()


speech()
while True:
    print('searching')
    sleep(4)
