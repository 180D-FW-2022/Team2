import glm
import pygame as pg
import numpy as np
import cv2
from pose import *
from utils import ARUCO_DICT

FOV = 20  # deg
NEAR = 0.01
FAR = 10
SPEED = 0.005
SENSITIVITY = 0.04


class Camera:
    def __init__(self, app, position=(0, 0, 1), yaw=-90, pitch=0, k=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch

        calibration_matrix_path = '../camera_matrix_laptop.npy'
        distortion_coefficients_path = '../distortion_matrix_laptop.npy'
        k = np.load(calibration_matrix_path)
        d = np.load(distortion_coefficients_path)

        h = 720
        fy = k[1][1]
        fov_y = 2* np.arctan2(h, 2 * fy)
        self.fov = np.deg2rad(40)
        print(np.rad2deg(self.fov))

        #frame = cv2.imread('../test_files/t2.jpg')
        #frame, rvecs, tvecs = pose_esitmation(frame, ARUCO_DICT['DICT_4X4_50'], k, d)

        #print(rvecs)
        #print(tvecs)

        # view matrix
        print('\nView Matrix:')

        rvecs = np.array([[[3.1415/2, -3.1415/2, -3.1415/2]]])
        tvecs = np.array([[[.1, -0.3, -1]]])

        rmtx = cv2.Rodrigues(rvecs)[0]

        view_matrix = np.array([[rmtx[0][0], rmtx[0][1], rmtx[0][2], tvecs[0][0][0]],
                                [rmtx[1][0], rmtx[1][1], rmtx[1][2], tvecs[0][0][1]],
                                [rmtx[2][0], rmtx[2][1], rmtx[2][2], tvecs[0][0][2]],
                                [0.0, 0.0, 0.0, 1.0]])
        # view_matrix = np.array([[1, 0, 0, 0],
        #                         [0, 1, 0, 0],
        #                         [0, 0, 1, 0],
        #                         [0.0, 0.0, 0.0, 1.0]])



        # INVERSE_MATRIX = (np.array([[1.0, 1.0, 1.0, 1.0],
        #                            [-1.0, -1.0, -1.0, -1.0],
        #                            [-1.0, -1.0, -1.0, -1.0],
        #                            [1.0, 1.0, 1.0, 1.0]]))


        # view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = glm.mat4x4(view_matrix)
        # view_matrix = np.transpose(view_matrix)
        view_matrix = self.get_view_matrix()

        self.m_view = view_matrix  # [R|t]

        print(self.m_view)
        # projection matrix
        # A = NEAR + FAR
        # B = NEAR * FAR
        # persp = np.array([[k[0][0], k[0][1], -k[0][2], 0],
        #                   [0, k[1][1], -k[1][2], 0],
        #                   [0, 0, A, B],
        #                   [0, 0, -1, 0]])

        persp = np.array([[2*k[0][0]/1280, -2*k[0][1]/1280, (1280 - 2*k[0][2])/1280, 0],
                          [0, 2*k[1][1]/720, (-720+2*k[1][2])/720, 0],
                          [0, 0, (-FAR - NEAR)/(FAR-NEAR), -2*FAR*NEAR/(FAR-NEAR)],
                          [0, 0, -1, 0]])

        persp = glm.mat4x4(persp)
        #gl_ortho = glm.ortho(-640, 640, 0, 720, NEAR, FAR)
        #gl_ortho = glm.ortho(0, 1280, 0, 720, NEAR, FAR)

        #self.m_proj = glm.mul(gl_ortho, persp)
        self.m_proj = persp
        print("\nProj Matrix:")
        print(self.m_proj)

        print("\nProj Matrix:")
        #print(self.get_projection_matrix())
        #self.m_proj = self.get_projection_matrix()
        # self.m_proj = cv2.rod

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update_camera_demo(self, rvecs, tvecs):
        if len(rvecs) == 0:
            return

        rmtx = cv2.Rodrigues(rvecs)[0]
        view_matrix = np.array([[rmtx[0][0], rmtx[0][1], rmtx[0][2], tvecs[0][0][0]],
                                [-rmtx[1][0], -rmtx[1][1], -rmtx[1][2], -tvecs[0][0][1]],
                                [-rmtx[2][0], -rmtx[2][1], -rmtx[2][2], -tvecs[0][0][2]],
                                [0.0, 0.0, 0.0, 1.0]])
        # view_matrix = np.array([[1, 0, 0, -0.1],
        #                         [0, 1, 0, 0],
        #                         [0, 0, 1, -0.2],
        #                         [0.0, 0.0, 0.0, 1.0]])

        # INVERSE_MATRIX = (np.array([[1.0, 1.0, 1.0, 1.0],
        #                             [1.0, 1.0, 1.0, -1.0],
        #                             [1.0, 1.0, 1.0, -1.0],
        #                             [1.0, 1.0, 1.0, 1.0]]))


        # view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = glm.mat4x4(view_matrix)
        # view_matrix = np.transpose(view_matrix)
        #view_matrix = self.get_view_matrix()
        self.m_view = view_matrix


    def update(self):
        self.move()
        self.rotate()
        # comment out to stop
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(self.fov, self.aspect_ratio, NEAR, FAR)




















