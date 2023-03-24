import moderngl as mgl
import numpy as np
import glm
import cv2
from PIL import Image


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        
        self.app = app
        self.pos = pos
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.offset = offset
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
        m_model = glm.translate(m_model, self.offset)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale, offset):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        # self.program['m_view_light'].write(self.app.light.m_view_light)
        # # resolution
        # self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        # # depth texture
        # self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        # self.program['shadowMap'] = 1
        # self.depth_texture.use(location=1)
        # # shadow
        # self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        # self.shadow_program = self.shadow_vao.program
        # self.shadow_program['m_proj'].write(self.camera.m_proj)
        # self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        # self.shadow_program['m_model'].write(self.m_model)
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
    
    def update_position(self, eye, center):
        x0 = eye[0]
        y0 = eye[1] * -1

        x1 = center[0]
        y1 = center[1] * -1

        # self.pos = (x0, 0, y0)

               
        m_model = glm.mat4()
        # rotate initial
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.scale(m_model, self.scale)
        m_model = glm.translate(m_model, self.offset)
        

        # rotate
        m_model = glm.inverse(glm.lookAt(glm.vec3(x0, 0, y0), glm.vec3(x1, 0, y1), glm.vec3(0, 1, 0))) * m_model

        
        

        # scale
        

        
       
        self.m_model = m_model


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)


class Plane(ExtendedBaseModel):
    def __init__(self, app, vao_name='plane', tex_id='grid', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)


class MovingCube(Cube):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rotate(self, t):
        rot = (0,t,0)
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.m_model = self.get_model_matrix()
    
    def update_loc(self, pos):
        self.pos = pos
        self.m_model = self.get_model_matrix()

    # def update(self):
    #     #self.m_model = self.get_model_matrix()
    #     super()

class Projectile(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0), eye=(0,0), center=(1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)
    def update_position(self, eye, center, t):
        self.pos = (self.pos[0], self.pos[1], -t)
        super().update_position(eye, center)
        return (self.m_model[3][0], -self.m_model[3][2])

class Cat(ExtendedBaseModel):
    def __init__(self, app, vao_name='cat', tex_id='cat',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)

## Props ##
class Tank(ExtendedBaseModel):
    def __init__(self, app, vao_name='tank', tex_id='tank',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)

class Container(ExtendedBaseModel):
    def __init__(self, app, vao_name='container', tex_id='container',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)

class Building1(ExtendedBaseModel):
    def __init__(self, app, vao_name='building1', tex_id='building1',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)

class Building2(ExtendedBaseModel):
    def __init__(self, app, vao_name='building2', tex_id='building2',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)


class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)
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
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

class BackgroundImage(BaseModel):
    def __init__(self, app, vao_name='background_image', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), offset=(0,0,0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, offset)

    def update(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, 0)
        img = Image.fromarray(img)

        ix = img.size[0]
        iy = img.size[1]
        img = img.tobytes()
        texture = self.app.ctx.texture(size=[ix, iy], components=3, data=img)
        texture.use()

    def render(self, img):
        self.update(img)
        self.vao.render()




















