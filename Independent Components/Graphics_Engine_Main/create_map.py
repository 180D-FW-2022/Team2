import cv2
import numpy as np
from tqdm import tqdm

arucoDict7 = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_50)
arucoDict6 = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
arucoParams = cv2.aruco.DetectorParameters_create()

mtx = np.load('../calibration/calibration_matrix_webcam.npy')
dist = np.load('../calibration/distortion_coefficients_webcam.npy')

# mtx = np.load('../calibration/camera_canon.npy')
# dist = np.load('../calibration/dist_canon.npy')

ARENA_WIDTH = 111.5
ARENA_HEIGHT = 96
VIEW_SCALE = 1.0



def calibrate_arena(vid, debug=False, num_samples=10):
    j = 0
    pbar = tqdm(total=num_samples)

    tl = np.array([0,0], dtype=np.float32)
    tr = np.array([0,0], dtype=np.float32)
    bl = np.array([0,0], dtype=np.float32)
    br = np.array([0,0], dtype=np.float32)

    while (j < num_samples):
        ret, frame = vid.read()
        h, w = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        
        
        corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict7,parameters=arucoParams)
        # use to debug marker detection
        if debug:
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            frame = cv2.resize(frame, (int(w*VIEW_SCALE), int(h*VIEW_SCALE)))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                debug=False
                cv2.destroyAllWindows()
            continue
        
        if len(corners) < 4:
            continue
  

        tl_index = np.where(ids == 0)[0][0]
        tr_index = np.where(ids == 1)[0][0]
        bl_index = np.where(ids == 2)[0][0]
        br_index = np.where(ids == 3)[0][0]
        
        for i in range(4):
            tl += corners[tl_index][0][i]/4
            tr += corners[tr_index][0][i]/4
            bl += corners[bl_index][0][i]/4
            br += corners[br_index][0][i]/4
            
        j += 1
        pbar.update(1)

    pbar.close()

    width = 700
    height = int(width*ARENA_HEIGHT/ARENA_WIDTH)

    offset = int(2.5 * width / ARENA_WIDTH)

    pts_src = np.array([tl, tr, bl, br])/num_samples
    pts_dst = np.array([[offset,offset], [width-offset,offset], [offset,height-offset], [width-offset,height-offset]])
    h, _ = cv2.findHomography(pts_src, pts_dst)
    return h

def process_frame_2(frame, homography, old_positions=None):
    positions = {}
    h, w = frame.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    
    corners_v, ids_v, rejected_v = cv2.aruco.detectMarkers(frame, arucoDict6,parameters=arucoParams)
    
    width = 700
    height = int(width*ARENA_HEIGHT/ARENA_WIDTH)
    img_warp = cv2.warpPerspective(frame, homography, (width,height))

    if len(corners_v) < 2:
        return img_warp, None, False

    v0 = np.array([0,0], dtype=np.float32)
    v0_index = np.where(ids_v == 0)[0][0]

    v1 = np.array([0,0], dtype=np.float32)
    v1_index = np.where(ids_v == 1)[0][0]
    
    for i in range(4):
        v0 += corners_v[v0_index][0][i]/4
        v1 += corners_v[v1_index][0][i]/4
    
    
    v0 = v0.reshape(-1,1,2)
    v0 = cv2.perspectiveTransform(v0, homography)[0][0].astype(int)
    v1 = v1.reshape(-1,1,2)
    v1 = cv2.perspectiveTransform(v1, homography)[0][0].astype(int)
    #v1 = v1 - [40, 40]

    scale_w = ARENA_WIDTH/width     # convert pixels to cm
    scale_h = ARENA_HEIGHT/height   # convert pixels to cm

    tolerence = .3 # 1mm threshold

    positions['tank'] = [(v0[0] * scale_w, ARENA_HEIGHT - v0[1] * scale_w), (v1[0] * scale_h, ARENA_HEIGHT - v1[1] * scale_h)]

    if old_positions is not None:
        eye_difference = np.array(positions['tank'][0]) - np.array(old_positions['tank'][0])
        center_difference = np.array(positions['tank'][1]) - np.array(old_positions['tank'][1])
        if np.linalg.norm(eye_difference) < tolerence:
            positions['tank'][0] = old_positions['tank'][0]
            v0 = np.array([positions['tank'][0][0] / scale_w, height - positions['tank'][0][1]/scale_h]).astype(int)

        if np.linalg.norm(center_difference) < tolerence:
            positions['tank'][1] = old_positions['tank'][1]
            v1 = np.array([positions['tank'][1][0] / scale_w, height - positions['tank'][1][1]/scale_h]).astype(int)

    v1_color = color=(255,255,0)
    v2_color = color=(0,255,0)
    img_warp = cv2.putText(img=img_warp, text=f"({positions['tank'][0][0]:.2f}, {positions['tank'][0][1]:.2f})"\
                            ,org=(v0[0], v0[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=v1_color, thickness=3)
    img_warp = cv2.circle(img_warp, (v0[0],v0[1]), radius=3, color=v1_color, thickness=3)
    img_warp = cv2.circle(img_warp, (v1[0],v1[1]), radius=3, color=v2_color, thickness=3)
    img_warp = cv2.arrowedLine(img_warp, (v0[0],v0[1]), (v1[0],v1[1]), (0,0,255), 3)

    img_warp = cv2.resize(img_warp, (int(width*VIEW_SCALE), int(height*VIEW_SCALE)))

    return img_warp, positions, True


if __name__ == '__main__':
    vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    homography = calibrate_arena(vid, debug=True, num_samples=5)
    old_positions = None
    while(True):
        ret, frame = vid.read()
        
        frame, positions, ret = process_frame_2(frame, homography, old_positions)
        if ret:
            old_positions = positions
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()

    # while(True):
    #     ret, frame = vid.read()
    #     cv2.imshow('frame', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    
    # vid.release()
    # cv2.destroyAllWindows()