import numpy as np
from engine.component import Component

class Transform(Component):
    def __init__(self, game_object=None):
        super().__init__(game_object)
        self.position = np.zeros(3, dtype=float)
        self.rotation = np.zeros(3, dtype=float)  # Euler angles in degrees
        self.scale = np.ones(3, dtype=float)
    def get_matrix(self):
        # Compose transformation matrix (translation * rotation * scale)
        T = np.eye(4)
        T[:3, 3] = self.position
        # For simplicity, only support ZYX Euler rotation
        rx, ry, rz = np.radians(self.rotation)
        cx, sx = np.cos(rx), np.sin(rx)
        cy, sy = np.cos(ry), np.sin(ry)
        cz, sz = np.cos(rz), np.sin(rz)
        Rx = np.array([[1,0,0,0],[0,cx,-sx,0],[0,sx,cx,0],[0,0,0,1]])
        Ry = np.array([[cy,0,sy,0],[0,1,0,0],[-sy,0,cy,0],[0,0,0,1]])
        Rz = np.array([[cz,-sz,0,0],[sz,cz,0,0],[0,0,1,0],[0,0,0,1]])
        R = Rz @ Ry @ Rx
        S = np.eye(4)
        S[0,0], S[1,1], S[2,2] = self.scale
        return T @ R @ S
