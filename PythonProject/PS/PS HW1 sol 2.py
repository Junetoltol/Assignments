import numpy as np
import matplotlib.pyplot as plt

# 샘플 개수
n = 10000

# 균등분포 난수
u = np.random.rand(n)

# (1) 지수분포
lam = 2
x = -np.log(1 - u) / lam
x_sorted = np.sort(x)
ecdf_x = np.arange(1, n+1) / n
cdf_x = 1 - np.exp(-lam * x_sorted)

plt.plot(x_sorted, ecdf_x, label="ECDF")
plt.plot(x_sorted, cdf_x, label="이론 CDF")
plt.title("Exponential")
plt.legend()
plt.show()

# (2) 코시분포
y = np.tan(np.pi*(u - 0.5))
y_sorted = np.sort(y)
ecdf_y = np.arange(1, n+1) / n
cdf_y = (1/np.pi)*np.arctan(y_sorted) + 0.5

plt.plot(y_sorted, ecdf_y, label="ECDF")
plt.plot(y_sorted, cdf_y, label="이론 CDF")
plt.title("Cauchy")
plt.legend()
plt.show()

# (3) 주사위
z = np.floor(6*u).astype(int) + 1
z_sorted = np.sort(z)
ecdf_z = np.arange(1, n+1) / n
k = np.arange(1, 7)
cdf_z = k / 6

plt.step(z_sorted, ecdf_z, where='post', label="ECDF")
plt.step(k, cdf_z, where='post', label="이론 CDF")
plt.title("Dice")
plt.legend()
plt.show()
