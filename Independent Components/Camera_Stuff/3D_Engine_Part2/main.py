import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
import time

from utils import ARUCO_DICT
from pose import *
from webcam import Webcam

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
        self.light = Light()
        # camera
        calibration_matrix_path = '../AruCo/calibration_files/calibration_matrix_webcam.npy'
        calibration = np.load(calibration_matrix_path)
        self.camera = Camera(self,  k=calibration)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self, background):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene.render(background)
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self, k, d):
        # webcam = Webcam()
        # webcam.start()

        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(k, d, (1280, 720), 1, (1280, 720))

        while True:
            self.get_time()
            self.check_events()

            #ret, background= cap.read()

            background = cv2.imread('../test_files/center.png')
            #background, rvec, tvec = pose_esitmation(background, aruco_dict_type, k, d)

            rvec = np.array([[[3.1415/2, 3.1415/2, 3.1415/2]]])
            tvec = np.array([[[0.1,  0.3,  1.0]]])


            cv2.drawFrameAxes(background, k, d, rvec, tvec, 0.2)
            #background = cv2.undistort(background, k, d, None, newcameramtx)
            # rvec = rvec * transform
            # tvec = tvec * transform

            # self.camera.update_camera_demo(rvec, tvec)

            self.camera.update()
            self.render(background)
            self.delta_time = self.clock.tick(60)

        #cap.release()
if __name__ == '__main__':
    app = GraphicsEngine()

    aruco_dict_type = ARUCO_DICT['DICT_7X7_50']
    calibration_matrix_path = '../camera_matrix_laptop.npy'
    # distortion_coefficients_path = 'calibration_files/distortion_coefficients_webcam.npy'
    # calibration_matrix_path = 'calibration_matrix.npy'
    distortion_coefficients_path = '../distortion_matrix_laptop.npy'
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)
    app.run(k, d)






























