import numpy as np
import matplotlib.pyplot as plt

T = (2 * np.pi) / 3
Ws = 2 * np.pi / T
Wm = 1
Omega = np.linspace(-10, 10, 4001)
Xp = np.zeros_like(Omega)
Omega_fold = (Omega + Ws/2) % Ws - Ws/2
mask = np.abs(Omega_fold) <= Wm
Xp[mask] = (1/T) * (1 - np.abs(Omega_fold[mask]))
plt.figure(figsize=(10, 6))
plt.plot(Omega, Xp, linewidth=2)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel(r'$\Omega$ (rad/sec)')
plt.ylabel(r'$X_p(j\Omega)$')
plt.title(r'CTFT of Sampled Signal')
xticks = np.arange(-9, 10, 3)
plt.xticks(xticks)
plt.xlim([-10, 10])

plt.tight_layout()
plt.show()