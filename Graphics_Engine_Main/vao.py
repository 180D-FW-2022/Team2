from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])

        # plane vao
        self.vaos['plane'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['plane'])

        # shadow cube vao
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo = self.vbo.vbos['cube'])

        # plane vao
        self.vaos['shadow_plane'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo = self.vbo.vbos['plane'])

        # cat vao
        self.vaos['cat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cat'])

        # shadow cat vao
        self.vaos['shadow_cat'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cat'])

        ## PROPS ##
        # tank vao
        self.vaos['tank'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['tank'])
        self.vaos['shadow_tank'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['tank'])

        # container vao
        self.vaos['container'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['container'])
        self.vaos['shadow_container'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['container'])
        
        # building1 vao
        self.vaos['building1'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['building1'])
        self.vaos['shadow_building1'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['building1'])

        # building2 vao
        self.vaos['building2'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['building2'])
        self.vaos['shadow_building2'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['building2'])


        # skybox vao
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

        # background image vao
        self.vaos['background_image'] = self.get_vao(
            program=self.program.programs['background_image'],
            vbo=self.vbo.vbos['background_image'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()