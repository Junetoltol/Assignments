import numpy as np
import matplotlib.pyplot as plt
T = (3 / 2) * np.pi
Ws = 2 * np.pi / T
Wm = 1
#DTFT
omega = np.linspace(-4*np.pi, 4*np.pi, 4001) # DTFT 주파수 축
omega_fold = (omega + np.pi) % (2*np.pi) - np.pi
Xd = np.zeros_like(omega)

for k in [-1, 0, 1]:
    shifted_w = omega - k * 2 * np.pi

    val = (1/T) * np.maximum(0, 1 - np.abs(shifted_w)/T)
    Xd += val

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(omega, Xd, 'r', linewidth=2)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel(r'$\omega$ (rad)')
plt.ylabel(r'$|X_d(e^{j\omega})|$')
plt.title(r'DTFT with $T=3\pi/2$ (Aliasing Observed)')
plt.xlim([-3*np.pi, 3*np.pi])


#CTFT
Omega = np.linspace(-4, 4, 4001)

Xp = np.zeros_like(Omega)
K = 3
for k in range(-K, K + 1):
    tri = (1/T) * np.maximum(0, 1 - np.abs(Omega - k*Ws))
    Xp += tri

plt.subplot(2, 1, 2)
plt.plot(Omega, Xp, 'b', linewidth=2)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel(r'$\Omega$ (rad/sec)')
plt.ylabel(r'$|X_p(j\Omega)|$')
plt.title(r'CTFT of Sampled Signal (Aliasing Distortion)')
plt.axvline(Ws, color='g', linestyle=':', label=r'$\omega_s$')
plt.axvline(Wm, color='k', linestyle='--', label=r'$\omega_M$')
plt.legend()
plt.xlim([-3, 3])

plt.tight_layout()
plt.show()