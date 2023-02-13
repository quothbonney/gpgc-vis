# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import matplotlib.pyplot as plt
import numpy as np
import os
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import sys
import decode

ori = np.array(decode.read_gtif("../data/2048.tif"))

if not( 'app' in locals()):
    app = QtWidgets.QApplication([])

traces = dict()
# app = QtGui.QApplication(sys.argv)
w = gl.GLViewWidget()
w.opts['distance'] = 2000
w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
w.setGeometry(0, 0, 600, 600)
w.show()
# socket = s

# timer = QtCore.QTimer()
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


y = np.linspace(0, 511, 512) 
print(y)
x = np.linspace(0,511, 512)
print(x)
temp_z = ori[:(len(x)), :(len(y))] / 2
print("ori", temp_z)

cmap = plt.get_cmap('jet')

minZ=np.min(temp_z)
maxZ=np.max(temp_z)
rgba_img = cmap((temp_z-minZ)/(maxZ -minZ))


surf = gl.GLSurfacePlotItem(x=y, y=x, z=temp_z, colors = rgba_img )

surf.scale(10,10,10)
# surf.shader()['colorMap'] = np.array(list(np.linspace(-100, 100, 1000)))
w.addItem(surf)

if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
