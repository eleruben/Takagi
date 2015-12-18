import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from scipy.fftpack import fft, fftfreq

n = 2**9
f= 400 #Hz
dt = 1 / float(f*512) #Espaciado por puntos, 16 punto por periodo
t=np.linspace(0, (n-1)*dt, n)
y=np.sin(2*pi*f*t)-0.5*np.sin(2*pi*2*f*t)-0.2**np.sin(2*pi*4*f*t)+0.1*np.sin(2*pi*8*f*t)

Y=fft(y)/n
frq = fftfreq(n, dt)

print frq

plt.figure(2)
plt.subplot(211)
plt.plot(t,y)
#plt.plot(t, y, 'ko')
plt.xlabel('Tiempo (s)')
plt.ylabel('$y(t)$')
plt.subplot(212)
plt.vlines(frq, 0, abs(Y))

plt.show()