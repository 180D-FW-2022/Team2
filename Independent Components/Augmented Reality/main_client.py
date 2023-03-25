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
import socket
import json

USE_SKY_BOX = True
LOCK_CAMERA = False
USE_DEFAULT_SETTINGS = False
USE_PI_CAMERA = False
FIRST_POV = True
SHOW_DEBUG_MAP = True
CALIBRATE_DEBUG = False

SERVER_ADDRESS = "131.179.6.151"

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
                self.camera = Camera(self, position=(0, 1.25, 3), pitch=-90) # overhead
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

    def render(self, img=None, bullet=None):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene_renderer.render(img, bullet=bullet)
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run_no_camera(self):
        self.camera.update()
        bullet = {'t': -1, 'eye': (0,0), 'center': (1,1)}
        bullet_location = (0,0)
        obstacles = [(17.5,17.5,20,20)]
        while True:
            self.get_time()
            self.check_events()

            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE] and bullet['t'] == -1:
                bullet['t'] += 1

            if bullet['t'] > -1:
                bullet['t'] += 1
            
            if bullet['t'] > 50:
                bullet['t'] = -1
            
            if bullet is not None and bullet['t'] > -1:
                bullet_location = self.scene.bullet.update_position(bullet['eye'], bullet['center'], bullet['t'])
            
            for obstacle in obstacles:
                if bullet_location[0] > obstacle[0] and bullet_location[0] < obstacle[2] and bullet_location[1] > obstacle[1] and bullet_location[1] < obstacle[3]:
                    print('HIT')

            if not LOCK_CAMERA:
                self.camera.update()

            if USE_SKY_BOX:
                self.render(bullet=bullet)
            else:
                if USE_PI_CAMERA:
                    background = get_pi_frame()
                else:
                    background = cv2.imread('textures/background_test_pattern.png')
                self.render(background, bullet=bullet)
            
            self.delta_time = self.clock.tick(60)


    def run_with_camera(self):
        bullet_location = (0,0)
        obstacles = [(17.5,17.5,20,20)]
        background = cv2.imread('textures/background_test_pattern.png')

        host = SERVER_ADDRESS
        port = 5000  # socket server port number
        print(host)

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        bullet = None
                   
        while True:
            self.get_time()
            self.check_events()

            data_string = client_socket.recv(1024).decode()
            data_string = data_string.split('{')[-1]

            if data_string == "null":
                ret = False
            else:
                ret = True
                data_string = '{' + data_string
                #print(data_string)
                positions = json.loads(data_string)  # receive response


            if not LOCK_CAMERA and ret:
                if FIRST_POV:
                    cam_eye = positions['tank'][0]
                    cam_center = positions['tank'][1]
                    self.camera.update_first_pov(cam_eye, cam_center)
                    #self.camera.update()
                elif not FIRST_POV:
                    self.camera.update()

            # data_string = client_socket.recv(1024).decode()
            # print(data_string)
            # bullet = json.loads(data_string)
            
            # if bullet is not None and bullet['t'] > -1:
            #     bullet_location = self.scene.bullet.update_position(bullet['eye'], bullet['center'], bullet['t'])

            for obstacle in obstacles:
                if bullet_location[0] > obstacle[0] and bullet_location[0] < obstacle[2] and bullet_location[1] > obstacle[1] and bullet_location[1] < obstacle[3]:
                    print('HIT')
            
            # call render pass
            if USE_SKY_BOX:
                self.render(bullet=bullet)
            else:
                if USE_PI_CAMERA:
                    img = get_pi_frame()
                    if img is not None:
                        background = img
                else:
                    background = cv2.imread('textures/background_test_pattern.png')
                self.render(background, bullet=bullet)
            self.delta_time = self.clock.tick(60)
        vid.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = GraphicsEngine()
    #app.run()
    app.run_with_camera()
