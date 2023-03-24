from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object
        #
        # n, s = 30, 3
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))

        #add(Cat(app, pos=(0, 0, 0)))


        #add(Cat(app, pos=(0, 0, 0), rot=(-90, 0, 0), scale=(0.007, 0.007, 0.007)))
        #add(Cube(app, pos=(-0.01, -0.01, -1.0), rot=(0, 0, 0), scale=(0.005, 0.005, 0.05), tex_id='red'))

        # #axis
        # add(Cube(app, pos=(0.05, 0, 0.0), rot=(0, 0, 0), scale=(0.05, 0.005, 0.005), tex_id='red'))
        # add(Cube(app, pos=(0, 0.05, 0.0), rot=(0, 0, 0), scale=(0.005, 0.05, 0.005), tex_id='green'))
        # add(Cube(app, pos=(0, 0.0, 0.05), rot=(0, 0, 0), scale=(0.005, 0.00, 0.05), tex_id='blue'))

        #tank
        #add(Tank(app, pos=(0.05, 0, 0.0), rot=(0, 0, 0), scale=(1, 1, 1)))

        add(Tank(app, pos=(0.0, 0.0, 0.0), rot=(-90, 0, 0), scale=(.1, .1, .1)))
        add(Container(app, pos=(0.0, 0.0, 0.0), rot=(-90, 0, 0), scale=(.001, .001, .001)))
        #add(House(app, pos=(0.0, 0.0, 0.0), rot=(0, 0, 0), scale=(.001, .001, .001)))
        #add(Cube(app, pos=(0, 0, .3), rot=(0, 0, 0)))
    def render(self, background):
        for obj in self.objects:
            obj.render()
        self.skybox.render(background)
