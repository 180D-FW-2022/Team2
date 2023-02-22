import numpy as np
import cv2
import requests
import keyboard
import time

#camera_name = "131.179.29.217"
camera_name = "131.179.28.137/"
url = 'http://' + camera_name +'/html/cam_pic.php'
print(url)

def get_pi_frame():
    try:
        response = requests.get(url, verify=False, timeout = 0.1)
        img = cv2.imdecode(np.frombuffer(response.content, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.rotate(img, cv2.ROTATE_180)
        img = cv2.resize(img, (1280, 720))
        return img
    except:
        print('skipping')
        return None

def debug_stream():
    while True:
        start_time = time.time()
        img = get_pi_frame()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if img is None:
            continue
        print(time.time()-start_time)
        cv2.imshow('window', img)
        
def capture_imgs():
    i = 0
    while True:
        img = get_pi_frame()
        cv2.imshow('window', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if keyboard.is_pressed("s"):
            cv2.imwrite(f'{i}.png', img)
            i += 1

if __name__ == '__main__':
    debug_stream()
    img = get_pi_frame()
    img = np.array(img)
    print(img.shape)