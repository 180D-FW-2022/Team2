import cv2

# cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
# ret,frame = cap.read() # return a single frame in variable `frame`
#
# # gst_str = ("rtspsrc location={} latency={} ! rtph264depay ! h264parse ! omxh264dec ! "
# #                "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
# #                "videoconvert ! appsink").format(uri, latency, width, height)
#
# while(True):
#     print(frame)
#     cv2.imshow('img1',frame) #display the captured image
#     if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y'
#         # cv2.imwrite('images/c1.png',frame)
#         cv2.destroyAllWindows()
#         break
#
#
# cap.release()

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    cv2.imshow('img', frame)  # display the captured image
    if cv2.waitKey(1) & 0xFF == ord('q'): #save on pressing 'y'
        cv2.destroyAllWindows()
        break
cap.release()