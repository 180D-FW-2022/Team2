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

        #add(Cat(app, pos=(0, -2, -10)))

        add(Cat(app, pos=(0, 0, 0), rot=(-90, 0, 0), scale=(0.007, 0.007, 0.007)))
        # add(Square(app, pos=(-0.12, -0.019, -0.25), rot=(0, 0, -np.rad2deg(0.0051)), scale=(0.02, 0.02, 0.02)))
        #add(Cube(app, pos=(0, 0, 0), rot=(0, 0, 0)))
    def render(self, background):
        for obj in self.objects:
            obj.render()
        self.skybox.render(background)
