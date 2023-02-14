# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import OpenGL
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import matplotlib.pyplot as plt
import numpy as np
import os
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import sys
import decode

from OpenGL.GL import glEnable, glDisable, GL_DEPTH_TEST
from pyqtgraph.Qt.QtGui import QOpenGLShaderProgram

ori = np.array(decode.read_gtif("data/512.tif"))

if not( 'app' in locals()):
    app = QtWidgets.QApplication([])

traces = dict()
# app = QtGui.QApplication(sys.argv)
w = gl.GLViewWidget()
w.opts['distance'] = 10 
w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
w.setGeometry(0, 0, 600, 600)
w.show()
# socket = s

# timer = QtCore.QTimer()`
# timer.setInterval(1) # in milliseconds
# timer.start()
# timer.timeout.connect(onNewData)

# create the background grids
#gx is the y grid
#gz is the x gid
gx = gl.GLGridItem()
gx.rotate(90, 0, 1, 0)
gx.translate(0, 0, 0)
w.addItem(gx)
gz = gl.GLGridItem()
gz.translate(200, -1000, -500)
w.addItem(gz)
gx.scale(100, 10, 1000)
gz.scale(100, 10, 1000)
cmap2 = plt.get_cmap('jet')

def draw_surf():
    y = np.linspace(0, 511, 512) 
    x = np.linspace(0,511, 512)
    temp_z = ori[:(len(x)), :(len(y))] / 2

    cmap = plt.get_cmap('twilight_shifted_r')

    minZ=np.min(temp_z)
    maxZ=np.max(temp_z)
    img2 = cmap2((temp_z-minZ)/(maxZ -minZ))
    surf = gl.GLSurfacePlotItem(x=y, y=x, z=temp_z, colors = img2)
    #dcdsurf = gl.GLSurfacePlotItem(x=y, y=x, z=dcd_z, colors=img2  )
    #surf.setGLOptions('translucent')
    surf.setGLOptions('opaque')
    surf.scale(10,10,3)
    #dcdsurf.scale(10,10,10)
    #surf.shader()['colorMap'] = np.array(list(np.linspace(-100, 100, 1000)))
    surf.setDepthValue(0)
    w.addItem(surf)
    #w.addItem(dcdsurf)

def draw_surf1():
    y = np.linspace(0, 511, 512) 
    x = np.linspace(0,511, 512)
    temp_z = ori[:(len(x)), :(len(y))] / 2

    cmap = plt.get_cmap('twilight_shifted_r')
    cmap2 = plt.get_cmap('jet')

    minZ=np.min(temp_z)
    maxZ=np.max(temp_z)


    dcd_z = (np.array(decode.decompress("./1.gpgc.log", 512)) / 2) + 10 


    img2 = cmap2((temp_z-minZ)/(maxZ -minZ))
    dcdsurf = gl.GLSurfacePlotItem(x=y, y=x, z=dcd_z, colors=img2  )
    #surf.setGLOptions('opaque')
    #surf.scale(10,10,10)
    dcdsurf.scale(10,10,3)
    #surf.shader()['colorMap'] = np.array(list(np.linspace(-100, 100, 1000)))
    #surf.setDepthValue(0)
    w.addItem(dcdsurf)


def draw_surf2():
    y = np.linspace(0, 511, 512) 
    x = np.linspace(0,511, 512)
    temp_z = ori[:(len(x)), :(len(y))] / 2

    cmap = plt.get_cmap('twilight_shifted_r')
    cmap2 = plt.get_cmap('jet')

    minZ=np.min(temp_z)
    maxZ=np.max(temp_z)
    rgba_img = cmap((temp_z-minZ)/(maxZ -minZ))
    img2 = cmap2((temp_z-minZ)/(maxZ -minZ))


    dcd_z = (np.array(decode.decompress("./2.gpgc.log", 512)) / 2) + 10 

    img2 = cmap2((dcd_z-minZ)/(maxZ -minZ))

    dcdsurf = gl.GLSurfacePlotItem(x=y, y=x, z=dcd_z, colors=img2  )
    #surf.setGLOptions('opaque')
    #surf.scale(10,10,10)
    dcdsurf.scale(10,10,3)
    #surf.shader()['colorMap'] = np.array(list(np.linspace(-100, 100, 1000)))
    #surf.setDepthValue(0)
    w.addItem(dcdsurf)

def draw_surf3():
    y = np.linspace(0, 511, 512) 
    x = np.linspace(0,511, 512)
    temp_z = ori[:(len(x)), :(len(y))] / 2

    cmap = plt.get_cmap('twilight_shifted_r')
    cmap2 = plt.get_cmap('jet')

    minZ=np.min(temp_z)
    maxZ=np.max(temp_z)
    rgba_img = cmap((temp_z-minZ)/(maxZ -minZ))
    img2 = cmap2((temp_z-minZ)/(maxZ -minZ))


    dcd_z = (np.array(decode.decompress("./3.gpgc.log", 512)) / 2) + 10 

    img2 = cmap2((dcd_z-minZ)/(maxZ -minZ))

    dcdsurf = gl.GLSurfacePlotItem(x=y, y=x, z=dcd_z, colors=img2  )
    #surf.setGLOptions('opaque')
    #surf.scale(10,10,10)
    dcdsurf.scale(10,10,3)
    #surf.shader()['colorMap'] = np.array(list(np.linspace(-100, 100, 1000)))
    #surf.setDepthValue(0)
    w.addItem(dcdsurf)


def draw_mesh():
    y2 = np.linspace(0, 511, 128) 
    x2 = np.linspace(0,511, 128)
    dcd_z = (np.array(decode.decompress("./512.gpgc.log", 512)) / 2) + 10 
    for i in range(len(x2)):
        yi = np.array([y2[i]] * 128)
        xi = np.array([x2[i]] * 128)
        #z = 10 * np.cos(d + self.phase) / (d + 1)
        z = (dcd_z[i*4, :len(x2)*4:4])
        pts2 = np.vstack([xi, y2, z]).transpose()
        line = gl.GLLinePlotItem(pos=pts2, width=1) 
        line.setDepthValue(0)
        #line.setWidth(3)
        """color=pg.glColor(
                
            (i, len(x) * 1.3)), antialias=True)"""
        
        line.scale(10,10,3)
        w.addItem(line)

def handle_function_1():
    w.clear()
    draw_surf1()

def handle_function_2():
    w.clear()
    draw_surf2()

def handle_function_3():
    w.clear()
    draw_surf3()


# Create the buttons and add them to a QHBoxLayout
layout = QtWidgets.QHBoxLayout()
button1 = QtWidgets.QPushButton('1')
button2 = QtWidgets.QPushButton('2')
button3 = QtWidgets.QPushButton('3')

button1.clicked.connect(lambda: handle_function_1())
button2.clicked.connect(lambda: handle_function_2()) 
button3.clicked.connect(lambda: handle_function_3())
layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)

# Add the buttons and the plot to a QVBoxLayout
vlayout = QtWidgets.QVBoxLayout()
vlayout.addLayout(layout)
vlayout.addWidget(w)

# Create a main window and set the layout
window = QtWidgets.QWidget()
window.setLayout(vlayout)
window.show()

if __name__ == '__main__':
    import sys
    
    draw_surf()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
