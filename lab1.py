import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp
import math

def Rot2D(X, Y, Alpha):
    RX = X*np.cos(Alpha) - Y*np.sin(Alpha)
    RY = X*np.sin(Alpha) + Y*np.cos(Alpha)
    return RX, RY

R = 4
Omega = 1
t = sp.Symbol('t')
T = np.linspace(0, 10, 1000)

x = R*(Omega*t-sp.sin(Omega*t))
y = R*(1-sp.cos(Omega*t))
xC = R*Omega*t
Vx = sp.diff(x, t)
Vy = sp.diff(y, t)

X = np.zeros_like(T)
Y = np.zeros_like(T)
XC = np.zeros_like(T)
YC = R
VX = np.zeros_like(T)
VY = np.zeros_like(T)

for i in np.arange(len(T)):
    X[i] = sp.Subs(x, t, T[i])
    Y[i] = sp.Subs(y, t, T[i])
    XC[i] = sp.Subs(xC, t, T[i])
    VX[i] = sp.Subs(Vx, t, T[i])
    VY[i] = sp.Subs(Vy, t, T[i])

fig = plt.figure()

ax1 = fig.add_subplot(1, 1, 1)
ax1.axis('equal')
ax1.set(xlim=[-R, 12*R], ylim=[-R, 3*R])

ax1.plot(X, Y)
ax1.plot([X.min(), X.max()], [0, 0], 'black')

P, = ax1.plot(X[0], Y[0], marker='o')

Phi = np.linspace(0, 2*math.pi, 100)
Circ, =ax1.plot(XC[0]+R*np.cos(Phi), YC+R*np.sin(Phi), 'green')

VLine, = ax1.plot([X[0], X[0]+VX[0]], [Y[0], Y[0]+VY[0]], 'red')

ArrowX = np.array([-0.2*R, 0, -0.2*R])
ArrowY = np.array([0.1*R, 0, -0.1*R])
RArrowX, RArrowY = Rot2D(ArrowX, ArrowY, math.atan2(VY[0], VX[0]))
VArrow, = ax1.plot(RArrowX+X[0]+VX[0], RArrowY+Y[0]+VY[0], 'red')
def anima(i):
    P.set_data(X[i], Y[i])
    Circ.set_data(XC[i]+R*np.cos(Phi), YC+R*np.sin(Phi))
    VLine.set_data([X[i], X[i]+VX[i]], [Y[i], Y[i]+VY[i]])
    RArrowX, RArrowY = Rot2D(ArrowX, ArrowY, math.atan2(VY[i], VX[i]))
    VArrow.set_data(RArrowX+X[i]+VX[i], RArrowY+Y[i]+VY[i])
    return P, Circ, VLine, VArrow

anim = FuncAnimation(fig, anima, frames=1000, interval=4, repeat=False)

plt.show()