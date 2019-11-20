from control.matlab import *
import control
import matplotlib.pyplot as plt
import numpy as num
from sympy import *
from sympy import I
from numpy import arange
import math

G = control.tf([0, 2], [160, 89, 16.4, 1])  # Найквист
GG = num.logspace(-3, 3, 10000)
real, imag, freq = control.nyquist(G, GG)
real = list(real)
imag = list(imag)
y1 = []
x1 = []
y2 = []
x2 = []

for i in range(0, len(real)):  # запас по фазе
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
    if -0.0001 < imag[i] < 0.0001 and abs(real[i]) > 0.15:
        print("Запас по амплитуде - ", real[i], imag[i])
        plt.plot(real[i], imag[i], '-o')
        xx1, yy1 = [-1, -1], [0, -1.5]
        xx2, yy2 = [real[i], real[i]], [0, -1.5]
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
