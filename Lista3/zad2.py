import math
import time

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# zmienne pomocnicze
pointSize = 10
windowSize = 200
pixelMap = [[0.0 for y in range(windowSize)] for x in range(windowSize)]
tick = 0.0


# funkcja rysująca zawartość macierzy pixelMap
def paint():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    for i in range(windowSize):
        for j in range(windowSize):
            glColor3f(pixelMap[i][j], 1.0, 1.0)
            glVertex2f(0.5 + 1.0 * i, 0.5 + 1.0 * j)
    glEnd()
    glFlush()


# inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize * pointSize, windowSize * pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Newlist01")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# inicjalizacja wyświetlania
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0.0, windowSize, 0.0, windowSize)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutDisplayFunc(paint)
glutIdleFunc(paint)
glClearColor(1.0, 1.0, 1.0, 1.0)
glEnable(GL_PROGRAM_POINT_SIZE)
glPointSize(pointSize)


def cupdate(step=0.1):
    global tick
    ltime = time.perf_counter()
    if ltime < tick + step:
        return False
    tick = ltime
    return True


def punkt(x, y, col):
    global pixelMap
    if 0 <= x <= windowSize:
        if 0 <= y <= windowSize:
            pixelMap[x][y] = col


def solve(x1, x2, w2):
    alpha = w2 * 0.0175
    
    M1 = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]])
    M2 = np.array([
        [x1],
        [x2],
        [1]])
    X = M1@M2
    
    x = int(X[0])
    y = int(X[1])

    return x, y

def rectangle(x, y, col):
    global pixelMap
    w2 = 6.25
    if 0 <= x <= windowSize:
        if 0 <= y <= windowSize:
            xa,ya  = solve(x-10, y-20, w2)
            pixelMap[xa][ya] = col

            xb, yb = solve(x-10, y+20, w2)
            pixelMap[xb][yb] = col

            xc, yc = solve(x+10, y-20, w2)
            pixelMap[xc][yc] = col

            xd, yd = solve(x+10, y+20, w2)
            pixelMap[xd][yd] = col


def ff(x, u):  # równanie stanu
    r = 0.8
    u1 = u[0]
    u2 = u[1]
    w1 = (u1 + u2)/2
    w2 = (u2 - u1)/r
    return np.array([math.cos(x[2])*w1, math.sin(x[2])*w1, w2])


def uu(t):  # wejście obiektu
    return np.array([5, 10])


def gg(x, u):  # wyjście obiektu
    return np.array([x[0] * 10, x[1] * 10, x[2] * 10]).transpose()


def rk2(f, u, x, dt):  # Runge-Kutta 2
    k1 = dt * f(x, u)
    return x + dt * f(x + k1 / 2, u)


def rk4(f, u, x, dt):
    k1 = dt * f(x, u)
    k2 = dt * f(x + k1 / 2, u)
    k3 = dt * f(x + k2 / 2, u)
    return x + dt * f(x + k3, u)


x = np.array([0, 0, 0]).transpose()
y = gg(x, uu(tick))

while True:
    
    if cupdate() and tick < 20000:
        rectangle(int(windowSize / 2 + round(y[0])), int(windowSize / 2 + round(y[1])), 0.0)
        x = rk4(ff, uu(tick), x, 0.1)
        y = gg(x, uu(tick))
        rectangle(int(windowSize / 2 + round(y[0])), int(windowSize / 2 + round(y[1])), 1.0)
    paint()
    glutMainLoopEvent()
