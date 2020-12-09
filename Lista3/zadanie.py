from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import math

pointSize = 10
windowSize = 100
pixelMap = [[0.0 for y in range(windowSize)] for x in range(windowSize)]
tick = 0.0


#funkcja rysująca zawartość macierzy pixelMap
def paint():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(windowSize):
        for j in range(windowSize):
            glColor3f(pixelMap[i][j], 0.0, 0.0)
            glVertex2f(0.5 + 1.0*i, 0.5 + 1.0*j)
    glEnd()
    glFlush()

#inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize*pointSize, windowSize*pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b'Newlist01')
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

#inicjalizacja wyświetlnia
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

