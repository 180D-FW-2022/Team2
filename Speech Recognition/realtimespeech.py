from pocketsphinx import LiveSpeech

for phrase in LiveSpeech(): 
   if "right" in str(phrase):
      print("turning right")
   if "left" in str(phrase):
      print("turning left")
   if "shoot" in str(phrase):
      print("shooting")
   if "reload" in str(phrase):
      print("reloading")
