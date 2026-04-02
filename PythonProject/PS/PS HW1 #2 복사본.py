import matplotlib.pyplot as plt
import numpy as np

# 샘플 개수
n = 10000

# Uniform(0,1) 난수 생성
u = np.random.rand(n)

# (1) 지수분포 (lambda = 2)
val = 2
# 역변환 공식: X = -log(1 - U) / λ
x = -np.log(1 - u) / val

x_sorted = np.sort(x)
ecdf_x = np.arange(1, n + 1) / n
theoretical_cdf_x = 1 - np.exp(-val * x_sorted)

plt.plot(x_sorted, ecdf_x, label="ECDF", color='blue')
plt.plot(x_sorted, theoretical_cdf_x, '--', label="이론 CDF", color='red')
plt.title("Exponential Distribution (λ=2)")
plt.xlabel("x")
plt.ylabel("CDF")
plt.legend()
plt.grid(True)
plt.show()

# (2) 코시분포 (Cauchy)
# 역변환: Y = tan(π(U - 0.5))
y = np.tan(np.pi * (u - 0.5))

y_sorted = np.sort(y)
ecdf_y = np.arange(1, n + 1) / n
theoretical_cdf_y = (1 / np.pi) * np.arctan(y_sorted) + 0.5

plt.plot(y_sorted, ecdf_y, label="ECDF", color='green')
plt.plot(y_sorted, theoretical_cdf_y, '--', label="이론 CDF", color='orange')
plt.title("Cauchy Distribution (0,1)")
plt.xlabel("y")
plt.ylabel("CDF")
plt.legend()
plt.grid(True)
plt.show()

# (3) 주사위 시뮬레이션 (1~6)
# 0~1 구간을 6개로 나누고, 정수값 매핑
dice = np.floor(6 * u).astype(int) + 1

dice_sorted = np.sort(dice)
ecdf_dice = np.arange(1, n + 1) / n

# 이론적 CDF: 1/6, 2/6, ..., 6/6
k = np.arange(1, 7)
theoretical_cdf_dice = k / 6

plt.step(dice_sorted, ecdf_dice, where='post', label="ECDF", color='purple')
plt.step(k, theoretical_cdf_dice, '--', where='post', label="이론 CDF", color='gray')
plt.title("Dice")
plt.xlabel("Dice Value")
plt.ylabel("CDF")
plt.legend()
plt.grid(True)
plt.show()
