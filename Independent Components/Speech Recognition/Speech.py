import speech_recognition as sr
import cv2

# obtain audio from the microphone
r = sr.Recognizer()
shoot="shoot"
right="right"
left="left"
while True:
	with sr.Microphone() as source:
		audio = r.listen(source)
	try:
		if r.recognize_sphinx(audio)==shoot:
			print('you said shoot')
		if r.recognize_sphinx(audio)==right:
                	print('you said right')
		if r.recognize_sphinx(audio)==left:
                	print('you said left') 
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
