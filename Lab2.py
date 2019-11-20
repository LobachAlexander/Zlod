from control.matlab import *
import control
import matplotlib.pyplot as plt
import numpy as num
from sympy import *
from sympy import I
from numpy import arange
import math


# numZ = [0, 100]
# denZ = [160, 89, 16.4, 2]
# numR = [0, 1]
# denR = [160, 89, 16.4, 1]

def Lab2(numZ, denZ, numR, denR, n):
    w1 = tf(numZ, denZ)  # Передаточная и переходная функции
    y1, x1 = step(w1)
    print("\nПередаточная функция замкнутой САУ - ", w1)
    w2 = tf(numR, denR)
    y2, x2 = step(w2)
    print("\nПередаточная функция разомкнутой САУ - ", w2)

    plt.plot(x1, y1, "r", label="Название")
    plt.title("Переходная функция замкнутой системы")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.show()

    plt.plot(x2, y2, "r", label="Название")
    plt.title("Переходная функция разомкнутой системы")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.show()

    G = control.tf(numR, denR)  # Найквист
    GG = num.logspace(-3, 3, 10000)
    real, imag, freq = control.nyquist(G, GG)
    real = list(real)
    imag = list(imag)
    y = []
    x = []
    for i in range(-1, 2, 1):
        y.append(i)
    for i in range(-1, 2, 1):
        x.append(-1)
    plt.plot(x, y, "r")

    for i in range(0, len(real)):
        z = abs(complex(real[i], imag[i]))
        if 0.999 < z < 1.001 and real[i] < 0 and imag[i] < 0:
            fi = atan(imag[i] / real[i]) * 180 / math.pi
            print("Запас по фазе - ", real[i], imag[i])
            plt.plot(real[i], imag[i], '-x')
            print("Угол - ", fi)
            plt.plot()
            xx, yy = [0, real[i]], [0, imag[i]]
            plt.plot(xx, yy)
            break

    for i in range(0, len(real)):
        z = abs(complex(real[i], imag[i]))
        if -0.0001 < imag[i] < 0.0001 and abs(real[i]) > 0.05:
            print("Запас по амплитуде - ", real[i], imag[i])
            plt.plot(real[i], imag[i], '-o')
            xx1, yy1 = [-1, -1], [0, -1.1]
            xx2, yy2 = [real[i], real[i]], [0, -1.1]
            plt.plot(xx1, yy1, "r", xx2, yy2, "r")
            break

    phi = num.linspace(0, 2 * num.pi, 100)
    r = num.sqrt(1.0)
    x1 = r * num.cos(phi)
    x2 = r * num.sin(phi)
    plt.plot(x1, x2)
    plt.title("Диаграмма Найквиста")
    plt.plot(label="Название")
    plt.xlabel("+1")
    plt.ylabel("+j")
    plt.grid(True)
    plt.show()

    mag, phase, omega = bode(w1, dB=True)  # ЛАЧХ и ЛФЧХ
    plt.title("ЛАЧХ и ЛФЧХ")
    plt.grid(True)
    plt.show()

    print("Полюса - %s" % pole(w1))
    pzmap(w1)
    plt.title("Расположение полюсов на комплексной плоскости")
    plt.grid(True)
    plt.show()
    plt.figure()

    w = symbols("w", real=True)  # Годограф Михайлова
    if n == 1:
        z = factor(160 * (I * w) ** 3 + 89 * (I * w) ** 2 + 16.4 * I * w + 2)
    elif n == 2:
        z = factor(160 * (I * w) ** 3 + 89 * (I * w) ** 2 + 16.4 * I * w + 9.1225)
    elif n == 3:
        z = factor(160 * (I * w) ** 3 + 89 * (I * w) ** 2 + 16.4 * I * w + 10)
    zR = re(z)
    zIm = im(z)
    x = [zR.subs({w: q}) for q in arange(0, 100, 0.1)]
    y = [zIm.subs({w: q}) for q in arange(0, 100, 0.1)]
    print(z)
    plt.title("Годограф Михайлова")
    plt.axis([-150, 10, -45, 5])
    plt.plot(x, y)
    plt.grid(True)
    plt.show()

    if n == 1:
        Matrix = num.matrix([[89, 2], [160, 16.4]])
    elif n == 2:
        Matrix = num.matrix([[89, 9.1225], [160, 16.4]])
    elif n == 3:
        Matrix = num.matrix([[89, 10], [160, 16.4]])
    Det = num.linalg.det(Matrix)
    print("Уравнение - ", denZ, "\nМатрица - \n", Matrix)
    print(" Определитель - ", Det)


# Lab2([0, 100], [160, 89, 16.4, 2], [0, 1], [160, 89, 16.4, 1], 1)  # Начальная функция

# Lab2([0, 100], [160, 89, 16.4, 9.12245], [0, 8.12245], [160, 89, 16.4, 1], 2)   # Функция при Кос = Кос.пред.

# Lab2([0, 100], [160, 89, 16.4, 10], [0, 9], [160, 89, 16.4, 1], 3)   # Функция при Кос > Кос.пред.
