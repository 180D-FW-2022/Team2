import numpy as np
import urllib.request
import cv2

camera_name = "131.179.74.215"
stream = urllib.request.urlopen('http://' + camera_name +'/html/cam_pic.php')
print('http://' + camera_name +'/html/cam_pic.php')

# WINDOW_NAME = "Camera"
# cv2.namedWindow(WINDOW_NAME)
# cv2.startWindowThread()

bytes = stream.read(10024)
while True:
    bytes += stream.read(10024)
    a = bytes.find(b'\xff\xd8') #frame starting
    b = bytes.find(b'\xff\xd9') #frame ending
    # new frame is available
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        #do your CV stuff here

        cv2.imshow('window', frame)
        # #get the next frame by adding any new string to the end of the url, here we use a timestamp
        url = 'http://' + camera_name +'/html/cam_pic.php'
        stream = urllib.request.urlopen(url)
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y'
        # cv2.imwrite('images/c1.png',frame)
        cv2.destroyAllWindows()
        break