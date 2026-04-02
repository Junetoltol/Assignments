import numpy as np
import matplotlib.pyplot as plt

T = 2 * np.pi / 3

omega = np.linspace(-4*np.pi, 4*np.pi, 4001)

Xd = np.zeros_like(omega)
omega_fold = (omega + np.pi) % (2*np.pi) - np.pi
mask = np.abs(omega_fold) <= T
Xd[mask] = (1/T) * (1 - np.abs(omega_fold[mask]) / T)
plt.figure()
plt.plot(omega, Xd)
plt.grid(True)
plt.xlabel('ω')
plt.ylabel('X_d')
plt.title('DTFT of Sampled Signal')
plt.xlim([-4*np.pi, 4*np.pi])
plt.show()
