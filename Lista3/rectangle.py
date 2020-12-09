from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import math
import numpy as np

pointSize = 10
windowSize = 50
pixelMap = [[0.0 for y in range(windowSize)] for x in range(windowSize)]
tick = 0.0


#funkcja rozwiązująca macierz rotacji
def solve(x1, x2):
    angle = 45
    alpha = angle * 0.0175
    M1 = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]])
    M2 = np.array([
        [x1],
        [x2],
        [1]])
    X = M1@M2

    return X

#funkcja rozwiązująca macierz translacji
def solve_t(x1, x2):
    v = np.array([15, 20])
    X = [x1, x2]
    X[0] += v[0]
    X[1] += v[1]
    '''
    M1 = np.array([
        [1, 0, dx1],
        [0, 1, dx2],
        [0, 0, 1]])
    M2 = np.array([
        [x1],
        [x2],
        [1]])
    X = np.linalg.solve(M1, M2)
    '''
    return X
#funkcja rysująca zawartość macierzy pixelMap
def paint():
    glPointSize(pointSize)
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    

    x1 = -10
    x2 = -20
    x3 = 20
    x4 = 10
    odcinek(5, 5, 5, 10)
    odcinek(5, 10, 30, 30)
#prostokąt
    #glColor3f(1.0, 0.0, 0.0)
    #glVertex2f(x1, x2) #A
    #glVertex2f(x4, x2) #B
    #glVertex2f(x4, x3) #C
    #glVertex2f(x1, x3) #D
#rotacja
    #A = solve(x1, x2)
    #B = solve(x4, x2)
    #C = solve(x4, x3)
    #D = solve(x1, x3)

    
    #glColor3f(0.0, 0.0, 1.0)
    #glVertex2f(A[0], A[1])
    #glVertex2f(B[0], B[1])
    #glVertex2f(C[0], C[1])
    #glVertex2f(D[0], D[1])
#translacja
    #A_t = solve_t(x1, x2)
    #B_t = solve_t(x4, x2)
    #C_t = solve_t(x4, x3)
    #D_t = solve_t(x1, x3)

    #glColor3f(0.0, 1.0, 0.0)
    #glVertex2f(A_t[0], A_t[1])
    #glVertex2f(B_t[0], B_t[1])
    #glVertex2f(C_t[0], C_t[1])
    #glVertex2f(D_t[0], D_t[1])
    
    

    glEnd()
    glFlush()

#inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize*pointSize, windowSize*pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b'Rectangle')
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

#inicjalizacja wyświetlnia
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(-windowSize, windowSize, -windowSize, windowSize)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutDisplayFunc(paint)
glutIdleFunc(paint)
glClearColor(1.0, 1.0, 1.0, 1.0)
glEnable(GL_PROGRAM_POINT_SIZE)
glPointSize(pointSize)

def cupdate(step = 0.1):
    global tick
    ltime = time.perf_counter()
    if ltime < tick + step:
        return False
    tick = ltime
    return True

def odcinek(x1, y1, x2, y2):
    global pixelMap
    d = (y2 - y1) / (x2 - x1)
    if 1 > d > -1:
        # współczynnik kierunkowy
        # tutaj należy sprawdzić współczynnik kierunkowy,
        # żeby zidentyfikować w której części układu rysowany jest odcinek
        if x1 > x2:  # rysujemy od lewej do prawej
            xtmp = x1
            x1 = x2
            x2 = xtmp

            ytmp = y1
            y1 = y2
            y2 = ytmp
        y = y1  # początkowa wartość y
        for x in range(round(x1), round(x2) + 1):  # przechodzimy przez piksele od x1 do x2
            y = y + d
            dcx = x
            dcy = round(y)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMap[dcx][dcy] = 1.0
    else:
        x = x1
        d = (x2 - x1) / (y2 - y1)
        for y in range(round(y1), round(y2) + 1):  # przechodzimy przez piksele od x1 do x2
            x = x + d
            dcy = y
            dcx = round(x)
            if 0 <= dcy < windowSize:
                if 0 <= dcx < windowSize:
                    pixelMap[dcy][dcx] = 1.0
        
while True:
    if cupdate():
        tt = tick
        x = windowSize * math.cos(tick)
        y = windowSize * math.sin(tick)
        odcinek(windowSize/2, windowSize/2, 50 + x, 50 + y)
    paint()
    glutMainLoopEvent()

