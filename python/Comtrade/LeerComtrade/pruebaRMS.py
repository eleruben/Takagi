import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from scipy.fftpack import fft, fftfreq
from scipy.integrate import simps
import math

x=np.linspace(0,2*pi,32)
t=np.linspace(0,0.01667,32)

y=np.sin(2*pi*60*t)

y2=y**2

integral=simps(y2,t)
k=1/0.01667
rms=math.sqrt(k*integral)

print integral
print k*integral
print rms

plt.plot(t,y)
plt.show()