

class SceneRenderer:
    def __init__(self, app, use_sky_box=False):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

        self.use_sky_box = use_sky_box

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def main_render(self, img=None, bullet=None, targets=None):
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()

        if bullet is not None and bullet['t'] > -1:
            self.scene.bullet.render()

        if targets is not None:
            for target in targets:
                if target[1] == 3:
                    pos = (target[0], target[1], -target[2])
                    self.scene.target.update_loc(pos)
                    self.scene.target.render()


        if self.use_sky_box:
            self.scene.skybox.render()
        else:
            self.scene.background.render(img)


    def render(self, img=None, bullet=None, targets=None):
        self.scene.update()
        # pass 1
        #self.render_shadow()
        # pass 2
        self.main_render(img, bullet=bullet, targets=targets)

    def destroy(self):
        self.depth_fbo.release()

