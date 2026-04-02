import numpy as np
import matplotlib.pyplot as plt

# 시간 축 설정
t = np.linspace(-3*np.pi, 3*np.pi, 3000)  # 시간 범위 확장


# 원래 신호 (사각파)
x = np.sign(np.sin(t))

# 여러 N 값에 대한 푸리에 급수 근사
N_values = [5, 10, 50]
plt.figure(figsize=(10,6))
plt.plot(t, x, 'k', label="Original Square Wave")

for N in N_values:
    fs_approx = np.zeros_like(t)
    for k in range(1, N+1, 2):  # 홀수 항만
        fs_approx += (4/np.pi) * (1/k) * np.sin(k*t)
    plt.plot(t, fs_approx, label=f"N={N}")

plt.title("Gibbs Phenomenon in Fourier Series Approximation")
plt.xlabel("t")
plt.ylabel("x(t)")
plt.legend()
plt.grid(True)
plt.show()
