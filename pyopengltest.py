import numpy as np
import matplotlib.pyplot as plt
from pyopengl import OpenGL as gl
from pyopengl import GLUT as glut
from decode import read_gtif, decompress

ori = read_gtif("data/512.tif")

def draw_grid():
    grid_size = 1000
    grid_height = -10
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(0.5, 0.5, 0.5)
    for i in range(-grid_size, grid_size, 100):
        gl.glVertex3f(i, grid_height, -grid_size)
        gl.glVertex3f(i, grid_height, grid_size)
        gl.glVertex3f(-grid_size, grid_height, i)
        gl.glVertex3f(grid_size, grid_height, i)
    gl.glEnd()

def draw_lines():
    y2 = np.linspace(0, 511, 128) 
    x2 = np.linspace(0, 511, 128)
    dcd_z = (decompress("./512.gpgc.log", 512) / 2) + 10 
    gl.glLineWidth(2)
    for i in range(len(x2)):
        yi = np.array([y2[i]] * 128)
        xi = np.array([x2[i]] * 128)
        z = (dcd_z[i*4, :len(x2)*4:4])

        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glColor3f(1, 1, 1)
        for j in range(len(x2)):
            gl.glVertex3f(xi[j], y2[j], z[j])
        gl.glEnd()

def draw_surface():
    y = np.linspace(0, 511, 512) 
    x = np.linspace(0, 511, 512)
    temp_z = ori[:(len(x)), :(len(y))] / 2

    cmap = plt.get_cmap('twilight_shifted_r')
    cmap2 = plt.get_cmap('jet')

    minZ=np.min(temp_z)
    maxZ=np.max(temp_z)
    rgba_img = cmap((temp_z-minZ)/(maxZ -minZ))
    img2 = cmap2((temp_z-minZ)/(maxZ -minZ))

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_DEPTH_TEST)

    for i in range(len(x)-1):
        for j in range(len(y)-1):
            gl.glBegin(gl.GL_QUADS)
            gl.glColor4f(*img2[i][j], 0.5)
            gl.glVertex3f(x[i], y[j], temp_z[i][j])
            gl.glVertex3f(x[i+1], y[j], temp_z[i+1][j])
            gl.glVertex3f(x[i+1], y[j+1], temp_z[i+1][j+1])
            gl.glVertex3f(x[i], y[j+1], temp_z[i][j+1])
            gl.glEnd()
