from model import *
import glm

SHOW_CAMERA_PLACEHOLDER = False

class Scene:
    def __init__(self, app, use_sky_box=False):
        self.app = app
        self.objects = []
        self.load()
        self.bullet = Projectile(app, pos=(0, 3.45, 0), tex_id='test', scale=(0.1, 0.1, 20))
        self.target= MovingCube(app, pos=(15, 3.45, -15), rot=(-90, 0, 0), scale=(1, 1, 1), tex_id=0)


        # skybox
        if use_sky_box:
            self.skybox = AdvancedSkyBox(app)
        else:
            self.background = BackgroundImage(app)

    def add_object(self, obj):
        self.objects.append(obj)

        
    def load(self):
        app = self.app
        add = self.add_object

        # # floor
        # n, s = 20, 2
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))

        # # columns
        # for i in range(9):
        #     add(Cube(app, pos=(15, i * s, -9 + i), tex_id=2))
        #     add(Cube(app, pos=(15, i * s, 5 - i), tex_id=2))

        # # cat
        # add(Cat(app, pos=(0, -1, -10)))

        # self.moving_cube = MovingCube(app, pos=(0, 6, 8), scale=(3, 3, 3), tex_id=1)
        # add(self.moving_cube)

        # add(Cube(app, pos=(0, 0, 0), tex_id=2))
        # add(Cube(app, pos=(7.2, 0, 0), tex_id=2))
        # add(Cube(app, pos=(0, 0, 12.8), tex_id=2))
        # add(Cube(app, pos=(7.2, 0, 12.8), tex_id=2, scale =(.5,.5,.5)))

        # self.cube1 = MovingCube(app, pos=(0, 0, 0), tex_id=2)
        # add(self.cube1)

        add(Cube(app, pos=(0, 0, 0), tex_id='test', scale=(0.1, 1, 0.1)))     # 1mm x 1mm (0,0) BL
        # add(Cube(app, pos=(20, 0, 0), tex_id='test', scale=(0.1, 1, 0.1)))    # 1mm x 1mm (200, 0) BR
        # add(Cube(app, pos=(0, 0, -20), tex_id='test', scale=(0.1, 1, 0.1)))   # 1mm x 1mm (0, 200) TL

        self.tank = Tank(app, offset=(-.3, -15, 0), pos = (.25, -12, 0), rot=(-90,178,0), scale=(2, 2, 2))
        add(self.tank)
        if SHOW_CAMERA_PLACEHOLDER:
            self.camera_shape = Cube(app, pos=(0, 0, 0), tex_id='camera_shape', scale=(5/2, .1/2, 7/2))
            self.camera_placeholder = Cube(app, pos=(0, 5, -13.5), tex_id='test', scale=(2.4/2, 2.4/2, .1/2))
            

            add(self.camera_shape)   # 50mm x 77mm (0, 200) camera shape
            add(self.camera_placeholder)   # 24mm x 24mm x 1 (0, 200) camera shape
            

        #add grid
        #grid_scale = 225/10 # mm to cm
        grid_scale = 100

        a_width = 111.5
        a_height = 96

        add(Plane(app, pos=(0, 0, 0), rot=(-90, 0, 0), scale=(a_width, a_height, grid_scale)))

        #add(Plane(app, pos=(-2.5-10, 0, 2.5+10), rot=(-90, 0, 0), scale=(grid_scale, grid_scale, grid_scale)))

        # add(Tank(app, offset=(-.3, -12, 0), rot=(-90,178,0), scale=(.5, .5, .5)))
        #add(Container(app, offset=(0, 0, 0), rot=(-90,0,0), scale=(.01, .01, .01)))
        #add(Building1(app, offset=(0, 0, 0), rot=(0,0,0), scale=(.01, .01, .01)))
        #add(Building2(app, offset=(0, 550, 0), rot=(0,0,0), scale=(.005, .005, .005)))

        add(Container(app, offset=(0, 0, 0), rot=(-90,0,0), scale=(.03, .03, .03), pos=(73,0,-75)))
        add(Building1(app, offset=(0, 0, 0), rot=(0,-90,0), scale=(.04, .04, .04), pos=(85.5,0,-34))) # shack
        add(Building2(app, offset=(0, 550, 0), rot=(0,90,0), scale=(.015, .015, .015), pos=(43,0,-47.5))) # big building
        add(Cube(app, rot=(0, 0, 0), scale=(5,2,2.5), pos=(85, 2, -24)))  # big building


        

    def update(self, positions=None):
        self.target.rotate(self.app.time*50)
        if positions is not None:
            cam_eye = positions['tank'][0]
            cam_center = positions['tank'][1]
            self.tank.update_position(cam_eye, cam_center)
            if SHOW_CAMERA_PLACEHOLDER:
                self.camera_shape.update_position(cam_eye, cam_center)
                self.camera_placeholder.update_position(cam_eye, cam_center)
                
