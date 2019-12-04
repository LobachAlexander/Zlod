import math
import control.matlab as con
from control.matlab import *
import control.matlab as c
import matplotlib.pyplot as plt
import numpy as np


def Lab3(W1, W2, W3, W4):
    Wsum = W1 * W2 * W3 * W4
    W = Wsum / (1 + Wsum)
    print("\nПередаточная функция замкнутой САУ - ", W)
    timeline = [i for i in np.arange(0, 100, 0.4)]   # генератор списка
    y1, x1 = step(W, timeline)
    print(con.stepinfo(W, timeline))
    maxy = 0
    maxx = 0
    for i in range(0, len(y1)):                                         # Максимум
        if y1[i] > maxy:
            maxy = y1[i]
            maxx = x1[i]
    plt.plot(maxx, maxy, '-x')
    xx1, yy1 = [maxx, maxx], [maxy, 0]
    plt.plot(xx1, yy1, "purple", linestyle='-.', linewidth=1)

    infinityy = 0
    for i in range(0, len(y1)):
        if abs(y1[i] - infinityy) > 0.0001:
            infinityy = y1[i]
    print("Установившееся значение функции - ", infinityy)

    y2 = []
    x2 = []
    for i in range(0, 50, 1):
        highgr = 1.05 * infinityy
        y2.append(highgr)
    for i in range(0, 50, 1):
        x2.append(i)
    y3 = []
    x3 = []
    lowgr = 0.95 * infinityy
    for i in range(0, 50, 1):
        y3.append(lowgr)
    for i in range(0, 50, 1):
        x3.append(i)
    plt.plot(x1, y1, "r")
    plt.plot(x2, y2, "b", linestyle='--', linewidth=1.5)
    plt.plot(x3, y3, "b", linestyle='--', linewidth=1.5)

    ppx = []
    ppy = []
    for g in range(0, len(y1)):                                     # Время ПП
        if (y1[g] - lowgr) < 0.001:
            pptime = x1[g]
            ppygrek = y1[g]
            ppx, ppy = [pptime, pptime], [y1[g], 0]
    plt.plot(pptime, ppygrek, '-o')
    plt.plot(ppx, ppy, "green", linestyle='-.', linewidth=1)
    plt.title("Переходная функция замкнутой системы")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.show()

    aS = pole(W)
    print("\nПолюса - %s" % aS)
    pzmap(W)
    plt.title("Расположение полюсов на комплексной плоскости")
    plt.grid(True)
    plt.show()

    mag, phase, omega = bode(Wsum, dB=True)
    # for ss in range(0, len(mag)):                                                        # запас по фазе
    #     if abs(mag[ss]) < 10:
    #         omegas = omega[ss]
    #         mags = math.degrees(mag[ss])
    #         zapsx, zapsy = [0, omegas], [mags, mags]
    #         break
    # plt.plot(omegas, mags, '-o')
    # plt.plot(zapsx, zapsy, "purple", linestyle='-.', linewidth=1)
    #
    # for v in range(0, len(phase)):                                                        # запас по амплитуде
    #     if abs(math.degrees(phase[v]) + 180) < 5:
    #         omehal = omega[v]
    #         phasel = math.degrees(phase[v])
    #         zapx, zapy = [0, omehal], [phasel, phasel]
    #         break
    # plt.plot(omehal, phasel, '-o')
    # zapxx, zapyy = [omehal, omehal], [phasel, -90]
    # plt.plot(zapx, zapy, "green", linestyle='-.', linewidth=1)
    # plt.plot(zapxx, zapyy, "purple", linestyle='-.', linewidth=1)
    plt.show()

    """"""""""""""""""""""""""""""""""""""""""

    # GG = np.logspace(-3, 3, 10000)                    # Найквист
    # real, imag, freq = nyquist(Wsum, GG)
    # real = list(real)
    # imag = list(imag)
    #
    # for i in range(0, len(real)):  # запас по фазе
    #     z = abs(complex(real[i], imag[i]))
    #     if 0.999 < z < 1.001 and real[i] < 0 and imag[i] < 0:
    #         fi = math.atan(imag[i] / real[i]) * 180 / math.pi
    #         print("Запас по фазе - ", real[i], imag[i])
    #         plt.plot(real[i], imag[i], '-x')
    #         print("Угол - ", fi)
    #         plt.plot()
    #         xx, yy = [0, real[i]], [0, imag[i]]
    #         plt.plot(xx, yy)
    #         break
    #
    # for i in range(0, len(real)):
    #     if -0.0001 < imag[i] < 0.0001 and abs(real[i]) > 0.15:
    #         print("Запас по амплитуде - ", real[i], imag[i])
    #         plt.plot(real[i], imag[i], '-o')
    #         xx1, yy1 = [-1, -1], [0, -1.5]
    #         xx2, yy2 = [real[i], real[i]], [0, -1.5]
    #         plt.plot(xx1, yy1, "r", xx2, yy2, "r")
    #         break
    #
    # phi = np.linspace(0, 2 * np.pi, 100)
    # r = np.sqrt(1.0)
    # x11 = r * np.cos(phi)
    # x22 = r * np.sin(phi)
    # plt.plot(x11, x22)
    # plt.title("Диаграмма Найквиста")
    # plt.plot(label="Название")
    # plt.xlabel("+1")
    # plt.ylabel("+j")
    # plt.grid(True)
    # plt.show()

    """"""""""""""""""""""""""""""""""""""""""

    'ПРЯМЫЕ МЕТОДЫ ОЦЕНКИ'
    print("\nПРЯМЫЕ МЕТОДЫ ОЦЕНКИ")
    print("\033[34;1mВремя переходного процесса - ", pptime, " c\033[30;1m")
    delta = (maxy - infinityy) / infinityy * 100
    print("\033[34;1mПерегулирование - ", delta, " %\033[30;1m")
    N = 0
    A = []
    for y in range(0, len(y1)):
        if x1[y] < pptime and y1[y - 1] < y1[y] > y1[y + 1]:
            N += 1
            A.append(y1[y])
    print("Колебательность (N) - ", N)
    print("A1 = ", A[0])
    if len(A) > 1:
        Y = 1 - (A[1] / A[0])
        print("A2 = ", A[1], "\nСтепень затухания (Y) - ", Y)
    else:
        print("A2 = 0", "\nВторого максимума нет, степень затухания равна единице")
    print("Максимум функции - ", maxy, "\nВремя достижения максимума - ", maxx, " c")

    'МЕТОДЫ ОЦЕНКИ ПО КОРНЯМ'
    print("\nМЕТОДЫ ОЦЕНКИ ПО КОРНЯМ")
    amin = 0
    for i in range(0, len(aS)):
        if 0 > aS[i].real > aS[i - 1].real:
            amin = aS[i].real
            tpp = 3 / abs(amin)
        if 0 > aS[i].real < aS[i - 1].real and aS[i].imag != 0:
            amax = aS[i].real
            jwmax = aS[i].imag
            mu = abs(jwmax / amax)
            sigma = math.exp(math.pi / mu)
            psi = 1 - math.exp(-(2 * math.pi / mu))
    print("amin = ", amin)
    print("\033[34;1mВремя переходного процесса - ", tpp, " c\033[30;1m")
    print("amax = ", amax, "\njwmax = ", jwmax)
    print("\033[34;1mСтепень колебательности (мю) - ", mu, "\033[30;1m")
    print("\033[34;1mПеререгулирование переходной характеристики (сигма) - ", sigma, "\033[30;1m")
    print("Степень затухания (пси) - ", psi)

    # 'ПО ЛОГАРИФМИЧЕСКИХ ХАРАКТЕРИСТИКАМ'
    # g = scipy.Integrate.quad(W)
    # print(g)


Lab3(c.tf([1], [6.4, 1]), c.tf([4], [5, 1]), c.tf([25], [5, 1]), c.tf([325, 55, 13], [1, 0]))  # ПИД       Кд Кп Ки
# Lab3(c.tf([1], [6.4, 1]), c.tf([4], [5, 1]), c.tf([25], [5, 1]), c.tf([314, 67], [1]))  # ПД                 Кд Кп

# Lab3(c.tf([1], [6.4, 1]), c.tf([4], [5, 1]), c.tf([25], [5, 1]), c.tf([0.70403, 0.07041, 0.007041], [1, 0]))  # ПИД       Кд Кп Ки
