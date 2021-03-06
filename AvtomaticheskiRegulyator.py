from control.matlab import *
import control.matlab as c
import math

W1 = c.tf([1], [6.4, 1])
W2 = c.tf([4], [51, 1])
W3 = c.tf([2228], [5, 1])


def hi(P, I, D):
    W4 = c.tf([D, P, I], [1, 0])

    Wsum = W1 * W2 * W3 * W4
    W = Wsum / (1 + Wsum)

    y1, x1 = step(W)
    steps = x1[2] - x1[1]
    maxy = 0
    maxx = 0
    for i in range(0, len(y1)):  # Максимум
        if y1[i] > maxy:
            maxy = y1[i]
            maxx = x1[i]

    infinityy = y1[len(y1) - 1]

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

    ppx = []
    ppy = []
    pptime = 0
    for g in range(0, len(y1)):  # Время ПП
        if (y1[g] - lowgr) < 0.001:
            pptime = x1[g]
            ppygrek = y1[g]
            ppx, ppy = [pptime, pptime], [y1[g], 0]

    aS = pole(W)

    magZ, phaseZ, omegaZ = bode(W, dB=False)

    delta = (maxy - infinityy) / infinityy * 100
    N = 0
    A = []
    for y in range(0, len(y1)):
        if x1[y] < pptime and y1[y - 1] < y1[y] > y1[y + 1]:
            N += 1
            A.append(y1[y])
    if len(A) > 1:
        Y = 1 - (A[1] / A[0])
    else:
        print()


    amin = 0
    for i in range(0, len(aS)):
        if 0 > aS[i].real > aS[i - 1].real:
            amin = aS[i].real
        if 0 > aS[i].real < aS[i - 1].real and aS[i].imag != 0:
            amax = aS[i].real
            jwmax = aS[i].imag
            mu = abs(jwmax / amax)
            if mu > 0.01:
                sigma = math.exp(math.pi / mu)
            else:
                print("Мю оч маленькое, сигма не расчитывается")

    Amax = 0
    for i in range(0, len(magZ)):
        if abs(magZ[i] - magZ[0]) < 0.05:
            omegasr = omegaZ[i]
        if magZ[i] > Amax:
            Amax = magZ[i]
    M = Amax / (magZ[0] + 0.000000000001)
    epsilon = 0
    for i in range(0, len(y1)):
        epsilon = epsilon + (infinityy - y1[i] * steps) ** 2
    print("\033[35;1mПараметры регулятора : ")
    print("Время регулирования : ", pptime, ". Требуемое значение : 12c")
    print("Показатель колебательности : ", M, ". Требуемое значение : 1.4")
    print("Перерегулирование : ", delta, " %", ". Требуемое значение : 27%")
    print("Значения регулятора:", "\nP = ", P, "\nI = ", I, "\nD = ", D, "\n\033[30;1m")
    return pptime, M, delta, epsilon


def check(t, M, per):
    result = False
    if t < 12:
        if M < 1.22:
            if per < 27:
                result = True
    return result


def PID(P, I, D):
    complete = False
    while not complete:
        P1 = P + 0.001
        P2 = P
        P3 = P
        I1 = I
        I2 = I + 0.001
        I3 = I
        D1 = D
        D2 = D
        D3 = D + 0.001
        tr1, M1, per1, e1 = hi(P1, I1, D1)
        tr2, M2, per2, e2 = hi(P2, I2, D2)
        tr3, M3, per3, e3 = hi(P3, I3, D3)
        ans1 = check(tr1, M1, per1)
        ans2 = check(tr2, M2, per2)
        ans3 = check(tr3, M3, per3)
        if ans1:
            P = P1
            I = I1
            D = D1
            complete = True
        elif ans2:
            P = P2
            I = I2
            D = D2
            complete = True
        elif ans3:
            P = P3
            I = I3
            D = D3
            complete = True
        else:
            e_min = min(e1, e2, e3)
            if e_min == e1:
                P = P1
                I = I1
                D = D1
            elif e_min == e2:
                P = P2
                I = I2
                D = D2
            elif e_min == e3:
                P = P3
                I = I3
                D = D3
    print(P, I, D)
    return P, I, D


Pp, Ii, Dd = PID(0.00001, 0.00001, 0.00001)
print("Финальные значения регулятора:", "\nP = ", Pp, "\nI = ", Ii, "\nD = ", Dd)
