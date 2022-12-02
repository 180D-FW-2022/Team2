from pocketsphinx import LiveSpeech
import time

start = time.time()
for phrase in LiveSpeech(): 
   if str(phrase) == "right":
      print("turning right")
   elif str(phrase) == "left":
      print("turning left")
   elif str(phrase) == "shoot":
      print("shooting")
   elif str(phrase) == "reload":
      print("reloading")
   else:
      print("not a keyword")
   print(time.time()-start)
