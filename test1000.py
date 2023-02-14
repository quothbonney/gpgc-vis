from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph.opengl as gl
import numpy as np
from OpenGL.GL import glEnable, glDisable, GL_DEPTH_TEST

class CustomViewWidget(gl.GLViewWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.opts['distance'] = 10
        self.opts['elevation'] = 30
        self.opts['azimuth'] = 45

        # create some test data
        self.data = np.array([
            [0, 0, 0],
            [1, 1, 1],
            [2, 0, 0],
            [3, 1, 1],
            [4, 0, 0],
        ])

        # create a GLLinePlotItem with the test data
        self.line = gl.GLLinePlotItem(pos=self.data, width=3)

        # add the line plot to the view
        self.addItem(self.line)

        # create a custom shader program
        self.shader = QtGui.QOpenGLShaderProgram(self.context())

        # compile the vertex shader
        vertexShaderSource = """
            attribute vec3 position;
            void main() {
                gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
            }
        """
        vertexShader = QtGui.QOpenGLShader(QtGui.QOpenGLShader.Vertex)
        vertexShader.compileSourceCode(vertexShaderSource)

        # compile the fragment shader
        fragmentShaderSource = """
            void main() {
                gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
        """
        fragmentShader = QtGui.QOpenGLShader(QtGui.QOpenGLShader.Fragment)
        fragmentShader.compileSourceCode(fragmentShaderSource)

        # link the vertex and fragment shaders together into a program
        self.shader.addShader(vertexShader)
        self.shader.addShader(fragmentShader)
        self.shader.link()

    def paintGL(self):
        # enable depth testing
        glEnable(GL_DEPTH_TEST)

        # activate the custom shader program
        self.shader.bind()

        # render the line plot
        self.line.paint()

        # deactivate the custom shader program
        self.shader.release()

        # disable depth testing
        glDisable(GL_DEPTH_TEST)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = CustomViewWidget()
    widget.show()
    app.exec_()
