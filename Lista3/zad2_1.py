from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import math
import numpy as np

## zmienne pomocnicze
pointSize = 10
windowSize = 100
step = 0.1
t0 = 0
tf = 10

def solve_move(x3):

    r = 5
    u1 = 15
    u2 = 17 
    w1 = (u1 + u2)/2
    w2 = (u2 - u1)/r

    M1 = np.array([
        [np.cos(x3), 0],
        [np.sin(x3), 0],
        [0, 1]
    ])
    M2 = np.array([
        [w1],
        [w2]
    ])
    
    Y = M1@M2
    return Y

def rysuj():
    glPointSize(pointSize)
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(20, 20)
    
    '''
    angle = 5
    x1 = 50
    x2 = 50
    x3 = angle * 0.0175

    t = np.arange(t0, tf, step)
    for i in t:
        
        
        glVertex2f(int(x1), int(x2))
        
        Y = solve_move(x3)
        x1 = Y[0]
        x2 = Y[1]
        x3 = float(Y[2])

        '''
        

    glEnd()
    glFlush()

glutInit()
glutInitWindowSize(windowSize*pointSize, windowSize*pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b'Zadanie nr 2')
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

#inicjalizacja wyświetlnia
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0.0, windowSize, 0.0, windowSize)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutDisplayFunc(rysuj)
glutIdleFunc(rysuj)
glClearColor(1.0, 1.0, 1.0, 1.0)
glEnable(GL_PROGRAM_POINT_SIZE)
glPointSize(pointSize)
