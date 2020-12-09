from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import numpy as np
import math

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
    ltime = time.time()
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


def ortho(p, l, r, b, t, n, f):  # projekcja ortograficzna

    ret = [2 / (r - l) * p[0] + (r + l) / (l - r),
           2 / (t - b) * p[1] + (t + b) / (b - t),
           2 / (f - n) * p[2] + (f + n) / (n - f)]

    return ret


def persp(p, l, r, b, t, n, f):
    ret = [(2 * (p[0] * n - r * p[2]) / (r * p[2] - l * p[2]) + 1),
           (2 * (p[1] * n - p[2] * t) / (p[2] * t - p[2] * b)) + 1,
           1 - (2 * ((p[2] - f) / (n - f)))]
    return ret


def screen(p, width, height):  # przekształcanie na wymiary ekranu

    ret = [(width - 1) * (p[0] + 1) / 2, (height - 1) * (p[1] + 1) / 2]

    return ret


def odcinek3D(p1, p2, R, G, B):  # rysowanie odcinka w 3D

    p1o = persp(p1, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)
    p2o = persp(p2, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)

    p1s = screen([p1o[0], p1o[1]], windowSize, windowSize)
    p2s = screen([p2o[0], p2o[1]], windowSize, windowSize)

    odcinek(p1s[0], p1s[1], p2s[0], p2s[1], R, G, B)


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


# moja implementacja

# Zadanie 1

def punkt_1(p, R, G, B):
    odcinek3D(p, p, R, G, B)


def odcinek_1(p, p1, R, G, B):
    odcinek3D(p, p1, R, G, B)


def Trojkat_1(p1, p2, p3, R, G, B):
    odcinek3D(p1, p2, R, G, B)
    odcinek3D(p2, p3, R, G, B)
    odcinek3D(p3, p1, R, G, B)


def prostokat_1(p, p1, R, G, B):
    odcinek3D(p, [p1[0], p[1], p1[2]], R, G, B)
    odcinek3D(p, [p[0], p1[1], p[2]], R, G, B)
    odcinek3D(p1, [p[0], p1[1], p[2]], R, G, B)
    odcinek3D(p1, [p1[0], p[1], p1[2]], R, G, B)


def prostopadloscian_1(dlugoscbokuA, dlugoscbokuB, dlugoscbokuC, psrodek, rotx, roty, rotz, R, G, B):
    pkt = [[psrodek[0] - dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] - dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] - dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] + dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] + dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] + dlugoscbokuC],
           [psrodek[0] - dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] + dlugoscbokuC]]

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
    odcinek3D(pkt[0], pkt[3], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[7], pkt[4], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)


# zadanie 2

def obrot_zad_2(punkt, kat,wektor, srodek,p0, os):
    x = punkt[0]
    y = punkt[1]
    z = punkt[2]

    if os == 'x':
        nowypunkt = [x + srodek[0],
                     ((y * math.cos(kat)) - (z * math.sin(kat))) + srodek[1],
                     ((y * math.sin(kat)) + (z * math.cos(kat))) + srodek[2]
                     ]
    elif os == 'y':
        nowypunkt = [((x * math.cos(kat)) + (z * math.sin(kat))) + srodek[0],
                     y + srodek[1],
                     ((z * math.cos(kat)) - (x * math.sin(kat))) + srodek[2]
                     ]
    elif os == 'z':
        nowypunkt = [((x * math.cos(kat)) - (y * math.sin(kat))) + srodek[0],
                     ((x * math.sin(kat)) + (y * math.cos(kat))) + srodek[1],
                     z + srodek[2]
                     ]
    elif os == "prosta":

        jednostkowy = np.sqrt(wektor[0] ** 2 + wektor[1] ** 2 + wektor[2] ** 2)

        if jednostkowy != 1:

            wersor = wektor / jednostkowy

        wersor = np.array(wersor)
        M = [[wersor[0] ** 2 * (1 - np.cos(kat)) + np.cos(kat),
              wersor[0] * wersor[1] * (1 - np.cos(kat) - wersor[2] * np.sin(kat)),
              wersor[0] * wersor[2] * (1 - np.cos(kat)) + wersor[1] * np.sin(kat)],
             [wersor[0] * wersor[1] * (1 - np.cos(kat)) + wersor[2] * np.sin(kat),
              wersor[1] ** 2 * (1 - np.cos(kat) + np.cos(kat)),
              wersor[1] * wersor[2] * (1 - np.cos(kat)) - wersor[0] * np.sin(kat)],
             [wersor[0] * wersor[2] * (1 - np.cos(kat)) - wersor[1] * np.sin(kat),
              wersor[1] * wersor[2] * (1 - np.cos(kat) + wersor[0] * np.sin(kat)),
              wersor[2] ** 2 * (1 - np.cos(kat)) + np.cos(kat)]]

        M = np.array(M)
        punkt = np.array(punkt)
        punkt = punkt - p0
        punkt = M @ punkt.T
        punkt = punkt + np.array(p0)
        punkt = punkt.T

    return punkt




def szescian_zad_1(dlugoscboku, srodek,wektor,kat,p0, R, G, B, os):

    pkt = [[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]]

    print(np.array(pkt[1]) - np.array(pkt[0]))

    for i in range(8):
        pkt[i] = obrot_zad_2(pkt[i], kat, wektor,srodek,p0, os)

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


key_out = 0
flag1 = False
flag2 = False

def keyboard(bkey, x, y, set_param=0):
    global key_out
    global flag1
    global flag2

    key = bkey.decode('utf-8')
    # Projekcja

    if key == '1':
        key_out = 1
    elif key == '2':
        key_out = 2
    elif key == '3':
        key_out = 3
    elif key == '4':
        key_out = 4
    elif key == '5':
        key_out = 5
    elif key == '6':
        key_out = 6
    # Parametry
    elif key == "o":
        key_out = 10
    elif key == "p":
        key_out = 11

    elif key == "z":
            OP.l = OP.l + 1
            print("l", OP.l)
    elif key == "Z":
        OP.l -= 1
        print("L", OP.l)
    elif key == "x":
            OP.r += 1
            print("r", OP.r)
    elif key == "X":
            OP.r -= 1
            print("r", OP.r)


    elif key == "c":
            OP.b += 1
            print("b", OP.b)
    elif key == "C":
        OP.b -= 1
        print("b", OP.b)

    elif key == "v":
        OP.t += 1
        print("t:", OP.t)
    elif key == "V":
        OP.t -= 1
        print("t:", OP.t)

    elif key == "b":
        OP.n += 1
        print("N:", OP.n)
    elif key == "B":
        OP.n -= 1
        print("N:", OP.n)


    elif key == "n":
        OP.f += 1
        print("F", OP.f)
    elif key == "N":
        OP.f -= 1
        print("F:", OP.f)

    # Animacja

    elif key == "9":
        flag2 = False
        flag1 = True

    elif key == "0":
        flag1 = False
        flag2 = True
    elif key == "8":
        flag1 = False
        flag2 = False


    # Exit

    elif key == 'q':
        sys.exit()


# Program running

kat = 0
while True:


    p1 = [2, 2, 30]
    p2 = [5, 5, 40]
    p3 = [4, 4, 30]

    clearMap([0.0, 0.0, 0.0])

    glutKeyboardFunc(keyboard)
    # prostopadloscian_1(2, 5, 7, [2, 2, 30], 0.1, 0.1, 0.1, 1, 1, 1)
    if key_out == 1:
        szescian_zad_1(5, [0, 0, 30], kat,[1,1,1], 1, 1, 1, 'x')
    elif key_out == 2:
        szescian_zad_1(5, [0, 0, 30], kat,[1,1,1], 1, 1, 1, 'y')
    elif key_out == 3:
        szescian_zad_1(5, [0, 0, 50], kat, 1, 1, 1, 'prosta')
    elif key_out == 4:
        prostopadloscian_1(2, 5, 7, [2, 2, 30], 0.1, 0.1, 0.1, 1, 1, 1)
    elif key_out == 5:

        szescian_zad_1(5, [0, 0, 30],[-2.5,2.5,0], kat, [-2.5,2.5,0], 1, 1, 1, 'prosta')
        odcinek3D(p1,p2,1,1,1)

    if flag1 == True:
        kat = kat + 0.1
    if flag2 == True:
        kat = kat - 0.1

    paint()
    glutMainLoopEvent()
