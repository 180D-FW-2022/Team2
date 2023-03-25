import glm
import pygame as pg
import numpy as np

# special
FOV = 50  # deg
NEAR = 0.01
FAR = 20000
SPEED = 0.05
SENSITIVITY = 0.1

# # default
# FOV = 50  # deg
# NEAR = 1
# FAR = 10000
# SPEED = 0.02
# SENSITIVITY = 0.1

calibration_matrix_path = '../calibration/camera_pi.npy'

class Camera:
    def __init__(self, app, position=(0, 5, 30), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        #self.m_proj = self.get_projection_matrix()
        self.m_proj = self.get_projection_matrix_from_calibration()

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

    def update_first_pov(self, eye, center):
        x0 = eye[0]
        y0 = eye[1] * -1

        x1 = center[0]
        y1 = center[1] * -1

        m_translate = glm.translate(glm.mat4(), -1 * self.position)
        m_model = m_translate * glm.lookAt(glm.vec3(x0, 0, y0), glm.vec3(x1, 0, y1), glm.vec3(0, 1, 0))
        self.m_view = m_model

    def update(self):
        self.move()
        self.rotate()
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
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

    def get_projection_matrix_from_calibration(self):
        k = np.load(calibration_matrix_path)
        proj = np.array([[2*k[0][0]/1280, -2*k[0][1]/1280, (1280 - 2*k[0][2])/1280, 0],
                  [0, 2*k[1][1]/720, (-720+2*k[1][2])/720, 0],
                  [0, 0, (-FAR - NEAR)/(FAR-NEAR), -2*FAR*NEAR/(FAR-NEAR)],
                  [0, 0, -1, 0]])

        proj = glm.mat4x4(proj)

        return proj




















