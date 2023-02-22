import moderngl as mgl
import numpy as np
import glm
import cv2
from webcam import Webcam
from PIL import Image
import pygame as pg
from io import BytesIO

class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Square(ExtendedBaseModel):
    def __init__(self, app, vao_name='square', tex_id=3, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Cat(ExtendedBaseModel):
    def __init__(self, app, vao_name='cat', tex_id='cat',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Tank(ExtendedBaseModel):
    def __init__(self, app, vao_name='tank', tex_id='tank',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Container(ExtendedBaseModel):
    def __init__(self, app, vao_name='container', tex_id='container',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(100, 100, 100)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class House(ExtendedBaseModel):
    def __init__(self, app, vao_name='house', tex_id='house',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(100, 100, 100)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id=0,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self, background):
        #image = self.webcam.get_current_frame()
        # image = cv2.imread('../test_files/still_img.jpg')
        image = background

        bg_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        bg_image = cv2.flip(bg_image, 0)
        # bg_image = cv2.flip(bg_image, 1)
        bg_image = Image.fromarray(bg_image)
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes()
        texture = self.app.ctx.texture(size=[ix, iy], components=3,
                                       data=bg_image)
        texture.use()
        # m_view = glm.mat4(glm.mat3(self.camera.m_view))
        # self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        # self.webcam = Webcam()
        # self.webcam.start()

        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use()

    def render(self, background):
        self.update(background)
        self.vao.render()



















