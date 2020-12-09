import time

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

## zmienne pomocnicze
pointSize = 5
windowSize = 200
clearColor = [0.0, 0.0, 0.0]

pixelMapR = [[clearColor[0] for y in range(windowSize)] for x in range(windowSize)]
pixelMapG = [[clearColor[1] for y in range(windowSize)] for x in range(windowSize)]
pixelMapB = [[clearColor[2] for y in range(windowSize)] for x in range(windowSize)]


class OP:  # parametry projekcji
    l = -10
    r = 10
    b = -10
    t = 10
    n = 10
    f = 100

"""    while True:
        key = input("Which parameter would you like to change? ")
        if key in ["l", "r", "b", "t", "n", "f"]:
            while True:
                value = input("New value its: ")
                try:
                    val = float(value)
                    if key == "l":
                        l = value
                        break
                    elif key == "r":
                        r = value
                        break
                    elif key == "b":
                        b = value
                        break
                    elif key == "t":
                        t = value
                        break
                    elif key == "n":
                        n = value
                        break
                    elif key == "f":
                        f = value
                        break
                except ValueError:
                    print("Must be a float")
                    continue
            break
        elif key == 'q':
            break
        else:
            print("Not a correct parameter. Try again")
            continue"""


def clearMap(color):
    global pixelMapR, pixelMapG, pixelMapB
    for i in range(windowSize):
        for j in range(windowSize):
            pixelMapR[i][j] = color[0]
            pixelMapG[i][j] = color[1]
            pixelMapB[i][j] = color[2]


## funkcja rysująca zawartość macierzy pixelMap
def paint():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    for i in range(windowSize):
        for j in range(windowSize):
            glColor3f(pixelMapR[i][j], pixelMapG[i][j], pixelMapB[i][j])
            glVertex2f(0.5 + 1.0 * i, 0.5 + 1.0 * j)
    glEnd()
    glFlush()


## inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize * pointSize, windowSize * pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Lab04")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
## inicjalizacja wyświetlania
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
    ltime = time.clock()
    if ltime < tick + step:
        return False
    tick = ltime
    return True


def odcinek(x1, y1, x2, y2, R, G, B):  # odcinek w 2d
    global pixelMapR
    global pixelMapG
    global pixelMapB
    if x2 == x1 and y2 == y1:
        x1 = round(x1)
        y1 = round(y1)
        if 0 <= x1 < windowSize:
            if 0 <= y1 < windowSize:
                pixelMapR[x1][y1] = R
                pixelMapR[x1][y1] = G
                pixelMapR[x1][y1] = B
        return

    ony = False
    d1 = None
    d2 = None
    if x2 == x1:
        d2 = 0
    elif y2 == y1:
        d1 = 0
    else:
        d2 = (x2 - x1) / (y2 - y1)
        if not -1 < d2 < 1:
            d1 = 1 / d2
    if d1 is not None:
        d = d1
        if x1 > x2:
            xtmp = x1
            x1 = x2
            x2 = xtmp
            ytmp = y1
            y1 = y2
            y2 = ytmp
        y = y1 - d
        for x in range(round(x1), round(x2) + 1):
            y = y + d
            dcx = x
            dcy = round(y)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMapR[dcx][dcy] = R
                    pixelMapG[dcx][dcy] = G
                    pixelMapB[dcx][dcy] = B
    else:
        d = d2
        if y1 > y2:
            xtmp = x1
            x1 = x2
            x2 = xtmp
            ytmp = y1
            y1 = y2
            y2 = ytmp
        x = x1 - d
        for y in range(round(y1), round(y2) + 1):
            x = x + d
            dcy = y
            dcx = round(x)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMapR[dcx][dcy] = R
                    pixelMapG[dcx][dcy] = G
                    pixelMapB[dcx][dcy] = B


def punkt(x, y, R, G, B):  # punkt w 2d
    global pixelMapR, pixelMapG, pixelMapB
    if 0 <= x <= windowSize:
        if 0 <= y <= windowSize:
            pixelMapR[x][y] = R
            pixelMapG[x][y] = G
            pixelMapB[x][y] = B


def perspective(p, l, r, b, t, n, f):  # projekcja perspektywiczna
    ret = [(2 * (p[0] * n - r * p[2]) / (r * p[2] - l * p[2])) + 1,
           (2 * (p[1] * n - t * p[2]) / (t * p[2] - b * p[2])) + 1,
           1 - (2 * (p[2] - f) / (n - f))]
    return ret

def ortho(p, l, r, b, t, n, f): # projekcja ortograficzna

  ret = [2 / (r - l) * p[0] + (r + l) / (l - r),
        2 / (t - b) * p[1] + (t + b) / (b - t),
        2 / (f - n) * p[2] + (f + n) / (n - f)]

  return ret


def screen(p, width, height):  # przekształcanie na wymiary ekranu
    ret = [(width - 1) * (p[0] + 1) / 2, (height - 1) * (p[1] + 1) / 2]
    return ret


def odcinek3D(p1, p2, R, G, B):  # rysowanie odcinka w 3D
    p1o = ortho(p1, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)
    p2o = ortho(p2, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)

    p1s = screen([p1o[0], p1o[1]], windowSize, windowSize)
    p2s = screen([p2o[0], p2o[1]], windowSize, windowSize)

    odcinek(p1s[0], p1s[1], p2s[0], p2s[1], R, G, B)


def trojkat(p1, p2, p3, R, G, B):  # rysowanie trojkata w 3D

    odcinek3D(p1, p2, R, G, B)
    odcinek3D(p2, p3, R, G, B)
    odcinek3D(p3, p1, R, G, B)


def prostokat(plewygorny, prawydolny, R, G, B):
    plewydolny = [plewygorny[0], prawydolny[1], 0]
    prawygorny = [prawydolny[0], plewygorny[1], 0]

    odcinek3D(plewydolny, prawydolny, R, G, B)
    odcinek3D(prawydolny, prawygorny, R, G, B)
    odcinek3D(prawygorny, plewygorny, R, G, B)
    odcinek3D(plewygorny, plewygorny, R, G, B)


def szescian(dlugoscboku, srodek, rotx, roty, rotz, R, G, B):
    pkt = [[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]]

    for i in range(8):
        npkt = np.matmul(np.array([[1, 0, 0], [0, np.cos(rotx), -np.sin(rotx)],
                                   [0, np.sin(rotx), np.cos(rotx)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt

    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(roty), 0, np.sin(roty)], [0, 1, 0],
                                   [-np.sin(roty), 0, np.cos(roty)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt
    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(rotz), -np.sin(rotz), 0],
                                   [np.sin(rotz), np.cos(rotz), 0], [0, 0, 1]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt


    odcinek3D(pkt[0], pkt[1], R, G, B)
    odcinek3D(pkt[1], pkt[2], R, G, B)
    odcinek3D(pkt[2], pkt[3], R, G, B)
    odcinek3D(pkt[3], pkt[0], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[7], pkt[4], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)

def obrot_zad_2(p0, wektor, punkt, kat):
    jednostkowy = np.sqrt(wektor[0] ** 2 + wektor[1] ** 2 + wektor[2] ** 2)

    if jednostkowy != 1:
        wersor = wektor / jednostkowy
    wersor = np.array(wersor)
    M=[[wersor[0]**2*(1-np.cos(kat))+np.cos(kat),wersor[0]*wersor[1]*(1-np.cos(kat)-wersor[2]*np.sin(kat)),wersor[0]*wersor[2]*(1-np.cos(kat))+wersor[1]*np.sin(kat)],
       [wersor[0]*wersor[1]*(1-np.cos(kat))+wersor[2]*np.sin(kat),wersor[1]**2*(1-np.cos(kat)+np.cos(kat)),wersor[1]*wersor[2]*(1-np.cos(kat))-wersor[0]*np.sin(kat)],
       [wersor[0]*wersor[2]*(1-np.cos(kat))-wersor[1]*np.sin(kat),wersor[1]*wersor[2]*(1-np.cos(kat)+wersor[0]*np.sin(kat)),wersor[2]**2*(1-np.cos(kat))+np.cos(kat)]]

    M = np.array(M)
    punkt = np.array(punkt)
    punkt = punkt - p0
    punkt = M @ punkt.T
    punkt = punkt + np.array(p0)
    punkt = punkt.T
    return punkt

def szescian_zad_1(dlugoscboku, srodek, kat, wersor, p0, R, G, B ):
    pkt = [[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]]


    for i in range(8):
        pkt[i] = obrot_zad_2(p0, wersor, pkt[i], kat).tolist()

    odcinek3D(pkt[0], pkt[1], R, G, B)
    odcinek3D(pkt[1], pkt[2], R, G, B)
    odcinek3D(pkt[2], pkt[3], R, G, B)
    odcinek3D(pkt[3], pkt[0], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[7], pkt[4], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)

def prostopadloscian(dlugoscboku, srodek, rotx, roty, rotz, R, G, B):
    pkt = [[srodek[0] - dlugoscboku[0], srodek[1] - dlugoscboku[1], srodek[2] - dlugoscboku[2]],
           [srodek[0] + dlugoscboku[0], srodek[1] - dlugoscboku[1], srodek[2] - dlugoscboku[2]],
           [srodek[0] + dlugoscboku[0], srodek[1] + dlugoscboku[1], srodek[2] - dlugoscboku[2]],
           [srodek[0] - dlugoscboku[0], srodek[1] + dlugoscboku[1], srodek[2] - dlugoscboku[2]],
           [srodek[0] - dlugoscboku[0], srodek[1] - dlugoscboku[1], srodek[2] + dlugoscboku[2]],
           [srodek[0] + dlugoscboku[0], srodek[1] - dlugoscboku[1], srodek[2] + dlugoscboku[2]],
           [srodek[0] + dlugoscboku[0], srodek[1] + dlugoscboku[1], srodek[2] + dlugoscboku[2]],
           [srodek[0] - dlugoscboku[0], srodek[1] + dlugoscboku[1], srodek[2] + dlugoscboku[2]]]

    for i in range(8):
        npkt = np.matmul(np.array([[1, 0, 0], [0, np.cos(rotx), -np.sin(rotx)],
                                   [0, np.sin(rotx), np.cos(rotx)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt

    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(roty), 0, np.sin(roty)], [0, 1, 0],
                                   [-np.sin(roty), 0, np.cos(roty)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt
    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(rotz), -np.sin(rotz), 0],
                                   [np.sin(rotz), np.cos(rotz), 0], [0, 0, 1]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt

    odcinek3D(pkt[0], pkt[1], R, G, B)
    odcinek3D(pkt[1], pkt[2], R, G, B)
    odcinek3D(pkt[2], pkt[3], R, G, B)
    odcinek3D(pkt[3], pkt[0], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[7], pkt[4], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)




while True:
    clearMap([0.0, 0.0, 0.0])
    szescian(3, [2, 2, 30], 0.2, 0.1, 0.2, 1.0, 1.0, 1.0)
    p = [[-1, -2, 0], [7, 5, 0]]
    v = -p[0]
    odcinek3D(p[0] , p[1], 1.0, 1.0, 1.0)


    odcinek3D([1, 0, 0], [0, 0, 0], 1.0, 1.0, 1.0)
    odcinek3D([0, 1, 0], [0, 0, 0], 1.0, 1.0, 1.0)
    odcinek3D([0, 0, 1], [0, 0, 0], 1.0, 1.0, 1.0)

    paint()
    glutMainLoopEvent()
