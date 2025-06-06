import OpenGL.GL as gl
import numpy as np

# Renderer module placeholder
class Renderer:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        gl.glEnable(gl.GL_DEPTH_TEST)
        # TODO: Setup shaders, camera, etc.

    def render(self):
        gl.glClearColor(0.15, 0.16, 0.18, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Draw all objects in the scene
        for obj in self.scene_manager.get_game_objects():
            mesh = getattr(obj, 'mesh', None)
            if mesh == 'cube':
                self.draw_cube(obj.transform)
            elif mesh == 'plane':
                self.draw_plane(obj.transform)

    def draw_cube(self, transform):
        # Simple immediate mode cube (for demonstration)
        gl.glPushMatrix()
        m = transform.get_matrix().T
        gl.glMultMatrixf(m)
        gl.glColor3f(0.7, 0.7, 0.9)
        # Draw cube using quads
        gl.glBegin(gl.GL_QUADS)
        # Front
        gl.glVertex3f(-0.5, -0.5,  0.5)
        gl.glVertex3f( 0.5, -0.5,  0.5)
        gl.glVertex3f( 0.5,  0.5,  0.5)
        gl.glVertex3f(-0.5,  0.5,  0.5)
        # Back
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f( 0.5, -0.5, -0.5)
        gl.glVertex3f( 0.5,  0.5, -0.5)
        gl.glVertex3f(-0.5,  0.5, -0.5)
        # Left
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5, -0.5,  0.5)
        gl.glVertex3f(-0.5,  0.5,  0.5)
        gl.glVertex3f(-0.5,  0.5, -0.5)
        # Right
        gl.glVertex3f(0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, -0.5,  0.5)
        gl.glVertex3f(0.5,  0.5,  0.5)
        gl.glVertex3f(0.5,  0.5, -0.5)
        # Top
        gl.glVertex3f(-0.5, 0.5, -0.5)
        gl.glVertex3f( 0.5, 0.5, -0.5)
        gl.glVertex3f( 0.5, 0.5,  0.5)
        gl.glVertex3f(-0.5, 0.5,  0.5)
        # Bottom
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f( 0.5, -0.5, -0.5)
        gl.glVertex3f( 0.5, -0.5,  0.5)
        gl.glVertex3f(-0.5, -0.5,  0.5)
        gl.glEnd()
        gl.glPopMatrix()

    def draw_plane(self, transform):
        gl.glPushMatrix()
        m = transform.get_matrix().T
        gl.glMultMatrixf(m)
        gl.glColor3f(0.6, 0.8, 0.6)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(-1, 0, -1)
        gl.glVertex3f( 1, 0, -1)
        gl.glVertex3f( 1, 0,  1)
        gl.glVertex3f(-1, 0,  1)
        gl.glEnd()
        gl.glPopMatrix()
