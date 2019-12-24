import control.matlab as cm
import numpy as n
import math
import cmath
import matplotlib.pyplot as plt

P = 0  # 0.1
I = 0
D = 0  # 1.3

# W4 = c.tf([D, P, I], [1, 0])

W1 = cm.tf([1], [6.4, 1])
W2 = cm.tf([44], [5, 1])
W3 = cm.tf([25], [5, 1])
Wob = (W2 * W3 * W1)


def pid(P, I, D):
    Wr_p = cm.tf([0, P], [0, 1])
    Wr_i = cm.tf([0, I], [1, 0])
    Wr_d = cm.tf([D, 0], [0, 1])
    Wr = Wr_p + Wr_i + Wr_d
    W = cm.feedback((Wob * Wr), 1)
    T = [i for i in n.arange(0, 100, 0.1)]
    y, t = cm.step(W, T)
    step = t[2] - t[1]
    y_ust = y[len(y) - 1]

    y_max = -9999
    for i in range(0, len(y), 1):
        if y[i] - y_max > 0.0001:
            y_max = y[i]
            ind_max = i
            t_max = t[ind_max]

    d_y = y_ust * 0.05
    t_reg = 99999
    for i in range(0, len(y), 1):
        if 0.0002 > abs(y[len(y) - 1 - i] - y_ust) - d_y > 0:
            y_reg = (y[len(y) - 1 - i])
            t_reg = (t[len(y) - 1 - i])
            break
    per = (y_max - y_ust) * 100 / y_ust

    num = W.num[0]
    den = W.den[0]
    num = num[0]
    den = den[0]
    amp = []
    phase = []
    freq = [i for i in n.arange(0, 100, 0.01)]  # формируем массив частот
    for i in range(0, len(freq), 1):
        num1 = 0
        den1 = 0
        for j in range(0, len(num), 1):
            num1 += num[j] * pow(complex(0, 1), len(num) - 1 - j) * pow(freq[i], len(num) - 1 - j)
        for k in range(0, len(den), 1):
            den1 += den[k] * pow(complex(0, 1), len(den) - 1 - k) * pow(freq[i], len(den) - 1 - k)
        amp.append(abs(num1 / (den1 + 0.0000000001)))
        phase.append(cmath.phase(num1 / (den1 + 0.0000000001)) * 180 / math.pi)

    max_amp = max(amp)
    ind = amp.index(max(amp))
    M = max_amp / (amp[0] + 0.000000001)
    print("Параметры регулятора : ")
    print("Время регулирования : ", t_reg, ". Требуемое значение : 15c")
    print("Показатель колебательности : ", M, ". Требуемое значение : 1.16")
    print("Перерегулирование : ", per, " %", ". Требуемое значение : 21%", '\n')
    kio = 0
    for i in range(0, len(y), 1):
        kio = kio + pow((y_ust - y[i] * step), 2)
    return t_reg, M, per, kio


def check(tr, M, per):
    result = False
    if tr < 15:
        if M < 1.16:
            if per < 21:
                result = True
    return result


def grad(P, I, D):
    complete = False
    while not complete:
        P1 = P + 0.1
        P2 = P
        P3 = P
        I1 = I
        I2 = I + 0.1
        I3 = I
        D1 = D
        D2 = D
        D3 = D + 0.1
        tr1, M1, per1, e1 = pid(P1, I1, D1)
        tr2, M2, per2, e2 = pid(P2, I2, D2)
        tr3, M3, per3, e3 = pid(P3, I3, D3)
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


Pf, If, Df = grad(P, I, D)
print(Pf, If, Df)
