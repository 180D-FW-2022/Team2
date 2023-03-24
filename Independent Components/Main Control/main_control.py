import cv2
import numpy as np
import keyboard
import socket
from pocketsphinx import LiveSpeech
import threading
from threading import Event
import json
import sys
import bluetooth
import time

COMMUNICATE = True
USE_BLUETOOTH = True


if USE_BLUETOOTH:
    # Bluetooth MAC address of Brian's raspberry pi
    bd_addr = "B8:27:EB:0E:7D:93"
    # Bluetooth MAC address of Gabe's raspberry pi
    #bd_addr = "B8:27:EB:4E:35:33"
    # Bluetooth MAC address of Gabe's raspberry pi
    #bd_addr = "B8:27:EB:84:75:48"
    # Bluetooth setup
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

# Sound and threading for sound
def recognizeshoot(event):
    global ammo
    global shoot
    global shoot_timer
    global reload_timer
    global shoot_ready
    speech = LiveSpeech(keyphrase='fire', kws_threshold=1e-2)
    for phrase in speech:
        print("shoot")
        if shoot_ready and ammo > 0 and shoot_timer == 5 and reload_timer == 40:
            shoot_ready = False
            shoot_timer = shoot_timer - 1
            ammo = ammo -1
            shoot = True
            if USE_BLUETOOTH:
                sock.send("y")
        if event.is_set():
            break

def recognizereload(event):
    global ammo
    global reload
    global shoot_timer
    global reload_timer
    global shoot_ready
    speech = LiveSpeech(keyphrase='load', kws_threshold=1e-2)
    for phrase in speech:
        print("reload")
        if not shoot_ready and ammo < 5 and shoot_timer == 5 and reload_timer == 40 and ammo > 0:
            shoot_ready = True
            reload_timer = reload_timer - 1
            # ammo = ammo + 1
            reload = True
            if USE_BLUETOOTH:
                sock.send("r")

time.sleep(4)
print("connect to graphics")

if COMMUNICATE:
    host = socket.gethostname()
    port_computer = 5000   # socket server port number
    # print(host)

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port_computer))  # connect to the server

print("completed connecting to graphics")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
arucoDict6 = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_50)
arucoParams = cv2.aruco.DetectorParameters_create()

# Rescaling video frame
_, frame = cap.read()
scale_percent = 50  # percent of original size
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)

r_img = cv2.imread('right.png')
l_img = cv2.imread('left.png')
r_img = cv2.flip(r_img, 0)
l_img = cv2.flip(l_img, 0)
r_d = r_img.shape[0]
pts_src = np.array([[0, 0], [r_d, 0], [r_d, r_d], [0, r_d]])

on = cv2.imread('on.png')
off = cv2.imread('off.png')

# print(height)
# print(width)

ammo = 5
shoot = False
reload = False

shoot_timer = 5
reload_timer = 40

space_down = True
r_down = True
shoot_ready = True
game_over = False

score = 0

stop_event = Event()
speech_shot = threading.Thread(target=recognizeshoot, args=(stop_event,), daemon=True)
speech_reload = threading.Thread(target=recognizereload, args=(stop_event,), daemon=True)
speech_shot.start()
speech_reload.start()


while (1):
    _, frame = cap.read()
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    if keyboard.is_pressed('space'):
        if not shoot and not space_down:
            if shoot_ready and ammo > 0 and shoot_timer == 5 and reload_timer == 40:
                shoot_ready = False
                ammo = ammo - 1
                shoot = True
                shoot_timer = shoot_timer - 1
                if USE_BLUETOOTH:
                    sock.send("y")
        space_down = True
    else:
        space_down = False

    if keyboard.is_pressed('r'):
        if not reload and not r_down:
            if ammo < 5 and reload_timer == 40 and shoot_timer == 5 and not shoot_ready and ammo > 0:
                shoot_ready = True
                # ammo = ammo + 1
                reload_timer = reload_timer - 1
                reload = True
                if USE_BLUETOOTH:
                    sock.send("r")
        r_down = True
    else:
        r_down = False


    corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict6, parameters=arucoParams)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.blur(frame, (3,3))
    frame = np.float32(frame)
    frame *= 0.5
    if shoot_timer < 5:
        frame = frame + frame*shoot_timer/5
    frame = np.uint8(frame)
    if shoot_timer < 5:
        frame = np.dstack([frame*0, frame*0, frame])
    else:
        frame = np.dstack([frame]*3)
    # frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    frame = cv2.line(frame, (0, int(height / 3)), (width, int(height / 3)), (113, 204, 46), 2)
    frame = cv2.line(frame, (0, int(height * 2 / 3)), (width, int(height * 2 / 3)), (113, 204, 46), 2)

    if score == 5:
        frame = cv2.imread('victory.png')
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        game_over = True
    elif ammo == 0 and shoot_timer == 5:
        frame = cv2.imread('over.png')
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        game_over = True


    command = ""
    if keyboard.is_pressed('e'):
        command += "q"
    elif keyboard.is_pressed('f'):
        command += "a"

    if keyboard.is_pressed('i'):
        command += "o"
    elif keyboard.is_pressed('j'):
        command += "l"

    if ids is not None:
        for i in range(len(ids)):
            corner_id = ids[i][0]
            center = [0, 0]
            pts_dst = []
            for j in range(4):
                center += corners[i][0][j] / 4
                pts_dst.append(corners[i][0][j])

            h = center[1]
            if corner_id == 0:
                img_in = r_img
                frame = cv2.line(frame, (0, int(h)), (width, int(h)), (219, 152, 52), 2)
                if "o" not in command and "l" not in command:
                    if h < height/3:
                        command += "o"
                    elif h > 2*height/3:
                        command += "l"

            elif corner_id == 1:
                img_in = l_img
                frame = cv2.line(frame, (0, int(h)), (width, int(h)), (34, 126, 230), 2)

                if "q" not in command and "a" not in command:
                    if h < height/3:
                        command += "q"
                    elif h > 2*height/3:
                        command += "a"

        for i in range(len(ids)):
            corner_id = ids[i][0]
            if corner_id == 0:
                img_in = r_img
            elif corner_id == 1:
                img_in = l_img
            else:
                continue

            pts_dst = []
            for j in range(4):
                pts_dst.append(corners[i][0][j])

            pts_dst = np.int32(pts_dst)
            matrix, _ = cv2.findHomography(pts_src, pts_dst)
            warped = cv2.warpPerspective(img_in, matrix, (width, height))
            mask = np.zeros((height, width), dtype="uint8")
            cv2.fillConvexPoly(mask, pts_dst, (255, 255, 255), cv2.LINE_AA)
            maskScaled = mask.copy() / 255.0
            maskScaled = np.dstack([maskScaled] * 3)
            warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
            imageMultiplied = cv2.multiply(frame.astype("float"), 1.0 - maskScaled)
            frame = cv2.add(warpedMultiplied, imageMultiplied)
            frame = frame.astype("uint8")

    frame = cv2.flip(frame, 1)

    # if command != "":
    #     print(command)

    if "q" in command:
        left = np.vstack((on, cv2.flip(off, 0)))
    elif "a" in command:
        left = np.vstack((off, cv2.flip(on, 0)))
    else:
        left = np.vstack((off, cv2.flip(off, 0)))

    if "o" in command:
        right = np.vstack((on, cv2.flip(off, 0)))
    elif "l" in command:
        right = np.vstack((off, cv2.flip(on, 0)))
    else:
        right = np.vstack((off, cv2.flip(off, 0)))
    frame = np.hstack((frame, left, right))


    if COMMUNICATE and not game_over:
        data = client_socket.recv(1024).decode()  # receive response
        game_state = json.loads(data)
        time = game_state['time']
        score = game_state['score']
        #print('Received from server: ' + data)  # show in terminal

        if shoot:
            data_string = "True"
        else:
            data_string = "False"
        client_socket.send(data_string.encode())  # send message
    elif not game_over:
        time = 0
        score = 0

    x = 220
    y = 200
    for i in range(5):
        if i < ammo:
            if reload_timer < 40:
                frame = cv2.rectangle(frame, (x+ i * 20, y+10), (x+i * 20 + 10, y+30), (0, 255*(40-reload_timer)/40, 0), -1)
            elif shoot_ready:
                frame = cv2.rectangle(frame, (x+ i*20,y+10), (x+i*20+10, y+30), (0, 255, 0), -1)
            else:
                frame = cv2.rectangle(frame, (x+ i*20,y+10), (x+i*20+10, y+30), (255, 255, 255), -1)
        else:
            if reload_timer < 40:
                frame = cv2.rectangle(frame, (x+ i * 20, y+10), (x+i * 20 + 10, y+30), (0, 110*(40-reload_timer)/40, 0), -1)
            else:
                frame = cv2.rectangle(frame, (x+ i * 20, y+10), (x+i * 20 + 10, y+30), (110, 110, 110), -1)

    if reload:
        reload = False
    if shoot:
        shoot = False

    if USE_BLUETOOTH:
        sock.send(command)

    frame = cv2.putText(frame, f'TIME: {time:05.1f}', (1, 17), cv2.FONT_HERSHEY_PLAIN, 1.3, (255, 255, 255), 1)
    frame = cv2.putText(frame, f'SCORE: {score:02d}', (207, 17), cv2.FONT_HERSHEY_PLAIN, 1.3, (255, 255, 255), 1)

    cv2.namedWindow('frame', 16)
    cv2.imshow('frame', frame)
    cv2.resizeWindow('frame', 470, 240)

    if shoot_timer == 0:
        shoot_timer = 5
    elif shoot_timer < 5:
        shoot_timer = shoot_timer -1

    if reload_timer == 0:
        reload_timer = 40
    elif reload_timer < 40:
        reload_timer = reload_timer -1

    # Press esc to exit
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
if COMMUNICATE:
    client_socket.close()  # close the connection
if USE_BLUETOOTH:
    sock.close()
sys.exit()