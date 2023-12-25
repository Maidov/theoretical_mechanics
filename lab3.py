import math
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


Steps = 1001
t_fin = 10
t = np.linspace(0, t_fin, Steps)  # Время

# Параметры системы
m1 = 5.0
m2 = 5.0
l = 1.0
b = 0.125
R = 0.25
g = 9.8
k = 10.0
phi0 = math.pi/2
omega0 = math.pi/2

def model(y, t):
    o, p, o_dot, p_dot = y
    do_dt = o_dot
    dp_dt = p_dot

    S = np.sin(o - p)
    C = np.cos(o - p)
    M = m1 + m2
    Mb = (m1 * b) / M
    Os = (do_dt ** 2) * S
    mbl = Mb / l
    gspl = (g * np.sin(p)) / l
    Ps = (dp_dt ** 2) * S
    r2b = (R ** 2) / (2 * b)
    rbb = r2b + b
    gso = g * np.sin(o)
    komb = (k * do_dt) / (m1 * b)
    U = (gso + komb) / l
    D = rbb / l
    W = (U + Ps) / C
    H = D / C
    G = C * mbl
    F = Os * mbl
    Y = F + gspl
    Z = G + H
    T = W - Y

    d2o_dt2_pre = ((-1) * T) / Z
    d2p_dt2 = d2o_dt2_pre * G - Y
    d2o_dt2 = (d2p_dt2 + Y)/G
    return [do_dt, dp_dt, d2o_dt2, d2p_dt2]

# Начальные условия
initial_conditions = [omega0, phi0, 0, 0]  # Начальные углы и скорости

# Решение системы уравнений
solution = odeint(model, initial_conditions, t)

o = solution[:, 0]  # Значения omega
p = solution[:, 1]    # Значения phi
do = solution[:, 2]
dp = solution[:, 3]

plt.subplot(2, 1, 1)
plt.plot(t, o, label='phi')
plt.plot(t, p, label='omega')
plt.title('Углы от времени')
plt.xlabel('Время')
plt.ylabel('Значение')
plt.legend()


plt.tight_layout()
plt.show()


phi1 = [x for x in p]
omega1 = [y for y in o]

def calculate_coordinates(radius, angle):
    x = radius * np.cos(np.radians(angle))
    y = radius * np.sin(np.radians(angle))
    return x, y



x5, y5 = -l / 2, l  # координата крепления левого подвеса A1
x6, y6 = l / 2, l  # координата крепления правого подвеса B1
x3, y3 = x5 + l * np.sin(p), y5 - l * np.cos(p)  # координата точки А, левый конец стержня
x4, y4 = x6 + l * np.sin(p), y6 - l * np.cos(p)  # координата точки B, левый конец стержня
x1, y1 = (x3 + x4) / 2, (y4 + y3) / 2  # Координаты крепления круга, точка O
x2, y2 = x1 + b * np.sin(o), y1 - b * np.cos(o)  # Координаты цетра круга, точка C


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.axis('equal')
ax.set_xlim(-2, 2)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Анимация подвешенного маятника')

drawed_AB = ax.plot([x3[0], x4[0]], [y3[0], y4[0]], 'g-', linewidth=2, label='Стержень ab')[0]
drawed_AA1 = ax.plot([x5, x3[0]], [y5, y3[0]], 'g-', linewidth=2, label='Подвес aa1')[0]
drawed_BB1 = ax.plot([x6, x4[0]], [y6, y4[0]], 'g-', linewidth=2, label='Подвес bb2')[0]
drawed_OC = ax.plot([x1[0], x2[0]], [y1[0], y2[0]], 'r-', linewidth=2, label='Круг OC')[0]

circle_OC = Circle((0, 0), R, color='r', fill=False, linestyle='-', linewidth=2, label='Круг OC')
ax.add_patch(circle_OC)

def update(frame):
    drawed_AB.set_data([x3[frame], x4[frame]], [y3[frame], y4[frame]])
    drawed_AA1.set_data([x5, x3[frame]], [y5, y3[frame]])
    drawed_BB1.set_data([x6, x4[frame]], [y6, y4[frame]])
    drawed_OC.set_data([x1[frame], x2[frame]], [y1[frame], y2[frame]])
    circle_OC.set_center((x2[frame], y2[frame]))


animation = FuncAnimation(fig, update, frames=len(t), interval=5)
plt.show()
