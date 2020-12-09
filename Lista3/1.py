from OpenGL.GL import *
from OpenGL.GLUT import *

def rysuj():
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

glutInit()
glutInitWindowSize(600, 400)
glutInitWindowPosition(0, 0)

glutCreateWindow(b'Zadanie nr 1')
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutDisplayFunc(rysuj)
glClearColor(1.0, 1.0, 1.0, 1.0)
glutMainLoop()