'''
Sample Usage:-
python pose_estimation.py --K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy --type DICT_5X5_100
'''


import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import time


def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera

    return:-
    frame - The frame with the axis drawn on it
    '''

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)

    # If markers are detected
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners) 

            # Draw Axis
            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)

    return frame, rvec, tvec

if __name__ == '__main__':
    aruco_dict_type = ARUCO_DICT['DICT_4X4_50']
    calibration_matrix_path = 'calibration_files/calibration_matrix_webcam.npy'
    #distortion_coefficients_path = 'calibration_files/distortion_coefficients_webcam.npy'
    #calibration_matrix_path = 'calibration_matrix.npy'
    distortion_coefficients_path = 'distortion_coefficients.npy'
    
    k = np.load(calibration_matrix_path)
    print(k)
    d = np.load(distortion_coefficients_path)
    print(d)

    # video = cv2.VideoCapture(0)
    # time.sleep(2.0)

    frame = cv2.imread('../test_files/still_img.jpg')
    output, rvec, tvec = pose_esitmation(frame, aruco_dict_type, k, d)

    cv2.imshow('Estimated Pose', output)

    cv2.waitKey(0)

    cv2.destroyAllWindows()