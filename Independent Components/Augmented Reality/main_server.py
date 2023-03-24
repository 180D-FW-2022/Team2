import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
import cv2
from create_map import *
from get_pi_video import *
from create_overlay import *
import socket
import json
import numpy as np
import bluetooth

USE_SKY_BOX = False
LOCK_CAMERA = False
USE_DEFAULT_SETTINGS = False
USE_PI_CAMERA = True
FIRST_POV = True
SHOW_DEBUG_MAP = True
CALIBRATE_DEBUG = False
USE_OVERLAY = False

USE_OVERHEAD_CAM = True

USE_MULTIPLAYER = True


class GraphicsEngine:
    def __init__(self, win_size=(1280, 720)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # light
        if USE_DEFAULT_SETTINGS:
            self.light = Light()
            self.camera = Camera(self)

        else:
            # unit meters
            # self.light = Light(position=(.1, 2, -.1))
            # self.camera = Camera(self, position=(0.1,0.3,-0.1), pitch=-90)

            # unit cm
            self.light = Light(position=(10, 20, -10))
            if FIRST_POV:
                #self.camera = Camera(self, position=(0, 1.25, 3), pitch=-90)
                #self.camera = Camera(self, position=(0, 5, -13.5), pitch=-90) # overhead
                self.camera = Camera(self, position=(0, 5.3, -10.3), pitch=-90)
            else:
                self.camera = Camera(self, position=(10,30,-10), pitch=-90) # overhead
                

        
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self, use_sky_box=USE_SKY_BOX)
        # renderer
        self.scene_renderer = SceneRenderer(self, use_sky_box=USE_SKY_BOX)
       
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()

    def render(self, img=None, bullet=None, targets=None):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene_renderer.render(img, bullet=bullet, targets=targets)
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run_no_camera(self):
        self.camera.update()
        bullet = {'t': -1, 'eye': (0,0), 'center': (1,1)}
        bullet_location = (0,0)
        obstacles = [(22.5, 25, 40, 67), (80, 21.5, 90, 39.5), (63, 72, 83, 80)]
        targets = [[15, 3, 15], [12, 3, 80], [95, 3, 80], [60, 3, 50], [80, 3, 10]]
        bullet_speed = 3

        game_dict = {'score': 0, 'time': 0}

        if USE_MULTIPLAYER:
            host = socket.gethostname()
            port = 5000   # initiate port no above 1024

            server_socket = socket.socket()
            server_socket.bind((host, port))

            # configure how many client the server can listen simultaneously
            server_socket.listen(1)
            conn, address = server_socket.accept()  # accept new connection
            print("Waiting for connection")
            print("Connection from: " + str(address))


        self.get_time()
        start_time = app.time
        while True:
            self.get_time()
            self.check_events()

            game_dict['time'] = app.time-start_time
            if USE_MULTIPLAYER:
                data_string = json.dumps(game_dict)
                conn.send(data_string.encode())  # send message
                fire = conn.recv(1024).decode()  # receive response
            else:
                fire = "False"

            if fire == "True":
                print("Fire")

            keys = pg.key.get_pressed()
            if fire == "True" and bullet['t'] == -1:
                bullet['t'] += 1

            if bullet['t'] > -1:
                bullet['t'] += bullet_speed
            
            if bullet['t'] > 50:
                bullet['t'] = -1

            if bullet is not None and bullet['t'] > -1:
                self.scene.bullet.update_position(bullet['eye'], bullet['center'], bullet['t'])
            
            if bullet['t'] == bullet_speed:
                bullet_direction = np.array([bullet['center'][0]-bullet['eye'][0], bullet['center'][1]-bullet['eye'][1]])
                #print(bullet_direction)
                for t in range(100):
                    bullet_pos = np.array(bullet['center']) + bullet_direction * t
                    #print(bullet_pos)
                    for obstacle in obstacles:
                        if bullet_location[0] > obstacle[0] and bullet_pos[0] < obstacle[2] and bullet_pos[1] > obstacle[1] and bullet_pos[1] < obstacle[3]:
                            print('HIT')

                    for target in targets:
                        if target[1] < 3:
                            continue
                        dist_to_target = np.linalg.norm(np.array([bullet_pos[0]-target[0], bullet_pos[1]-target[2]]))
                        if dist_to_target < 2:
                            target[1] = -3
                            print('GOTEM')

            if not LOCK_CAMERA:
                self.camera.update()

            if USE_SKY_BOX:
                self.render(bullet=bullet, targets=targets)
            else:
                if USE_PI_CAMERA:
                    background = get_pi_frame()
                else:
                    background = cv2.imread('textures/background_test_pattern.png')
                self.render(background, bullet=bullet, targets=targets)
            
            self.delta_time = self.clock.tick(60)


    def run_with_camera(self):
        vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  
        bullet = {'t': -1, 'eye': (0,0), 'center': (1,1)}
        bullet_location = (0, 0)
        obstacles = [(22.5, 25, 40, 67), (80, 21.5, 90, 39.5), (63, 72, 83, 80)]
        targets = [[15, 3, 15], [12, 3, 80], [95, 3, 80], [60, 3, 50], [80, 3, 10]]
        background = cv2.imread('textures/background_test_pattern.png')
        bullet_speed = 25
        game_dict = {'score': 0, 'time': 0}

        best_time = 0
        victory = False 

        homography = calibrate_arena(vid, debug=CALIBRATE_DEBUG, num_samples=2)
        old_positions = None
        score = 0

        if USE_MULTIPLAYER:
            host = socket.gethostname()
            port = 5000  # initiate port no above 1024

            server_socket = socket.socket()
            server_socket.bind((host, port))

            # configure how many client the server can listen simultaneously
            server_socket.listen(1)
            conn, address = server_socket.accept()  # accept new connection
            print("Waiting for connection")
            print("Connection from: " + str(address))
        
        self.get_time()
        start_time = app.time  
        while True:
            self.get_time()
            self.check_events()

            _, frame = vid.read()
            frame, positions, ret = process_frame_2(frame, homography, old_positions=old_positions)
            if ret: 
                old_positions = positions

            game_dict['time'] = app.time - start_time
            if USE_MULTIPLAYER:
                data_string = json.dumps(game_dict)
                conn.send(data_string.encode())  # send message
                fire = conn.recv(1024).decode()  # receive response
            else:
                fire = "False"

            if fire == "True":
                print("Fire")

            if not LOCK_CAMERA:
                if FIRST_POV and ret:
                    cam_eye = positions['tank'][0]
                    cam_center = positions['tank'][1]
                    self.camera.update_first_pov(cam_eye, cam_center)
                    #self.camera.update()
                elif not FIRST_POV:
                    self.camera.update()
                    
            if ret:
                self.scene.update(positions)
                if bullet['t'] == -1:
                    bullet['eye'] = positions['tank'][0]
                    bullet['center'] = positions['tank'][1]

            if SHOW_DEBUG_MAP:
                frame = cv2.resize(frame, (286, 240))
                cv2.namedWindow('frame', 16)
                cv2.imshow('frame', frame)
                cv2.resizeWindow('frame', 286, 240)

            if fire == "True" and bullet['t'] == -1:
                bullet['t'] += 1

            if bullet['t'] > -1:
                bullet['t'] += bullet_speed
            
            if bullet['t'] > 50:
                bullet['t'] = -1

            # if USE_MULTIPLAYER:
            #     data_string = json.dumps(bullet)
            #     conn.send(data_string.encode())  # send message
            #     #data = conn.recv(1024).decode()  # receive response
            
            if bullet is not None and bullet['t'] > -1:
                bullet_location = self.scene.bullet.update_position(bullet['eye'], bullet['center'], bullet['t'])
            
            if bullet['t'] == bullet_speed:
                bullet_direction = np.array([bullet['center'][0]-bullet['eye'][0], bullet['center'][1]-bullet['eye'][1]])
                for t in range(200):
                    bullet_pos = np.array(bullet['center']) + bullet_direction * t*0.5
                    for obstacle in obstacles:
                        if bullet_location[0] > obstacle[0] and bullet_pos[0] < obstacle[2] and bullet_pos[1] > obstacle[1] and bullet_pos[1] < obstacle[3]:
                            print('HIT')

                    for target in targets:
                        if target[1] < 3:
                            continue
                        dist_to_target = np.linalg.norm(np.array([bullet_pos[0]-target[0], bullet_pos[1]-target[2]]))
                        if dist_to_target < 3:
                            target[1] = -3
                            print('GOTEM')
                            score += 1
                            game_dict['score'] += 1
                            # if score == len(targets):
                            #     best_time = app.time- start_time
                            #     victory = True
                            #     print(f'Victory! Time: {best_time:.2f}s')
                            #     cv2.destroyAllWindows()
                            break
            if USE_OVERLAY and not victory:
                overlay = create_overlay(app.time-start_time, score)
                cv2.imshow('status', overlay)

            
            # call render pass
            if victory:
                background = victory_screen(best_time-start_time)
                self.render(background, bullet=bullet, targets=targets)
            elif USE_SKY_BOX:
                self.render(bullet=bullet, targets=targets)
            else:
                if USE_PI_CAMERA:
                    img = get_pi_frame()
                    if img is not None:
                        background = img
                else:
                    background = cv2.imread('textures/background_test_pattern.png')
                self.render(background, bullet=bullet, targets=targets)
            self.delta_time = self.clock.tick(60)
        vid.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = GraphicsEngine()
    if USE_OVERHEAD_CAM :
        app.run_with_camera()
    else:
        app.run_no_camera()
    
