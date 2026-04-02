import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(-20, 20, 1000)
x = np.zeros_like(t)
mask = np.abs(t) > 1e-10
x[mask] = (1 - np.cos(t[mask])) / (np.pi * t[mask]**2)
x[~mask] = 1 / (2 * np.pi)

plt.figure(figsize=(10, 6)) # 그래프 크기 설정
plt.plot(t, x, label=r'$x(t) = \frac{1-\cos(t)}{\pi t^2}$', linewidth=2)
plt.title('Inverse Fourier Transform of Triangular Spectrum')
plt.xlabel('Time (t)')
plt.ylabel('Amplitude')
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()