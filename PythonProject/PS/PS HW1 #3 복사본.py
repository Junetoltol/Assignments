import math

import matplotlib.pyplot as plt
import numpy as np

A = 1.0              # 송신 '1'의 전압
sigma2 = 0.1         # 잡음 분산
sigma = np.sqrt(sigma2)

# 사전확률 (B: 균등, C: 비균등)
P0_eq, P1_eq = 0.5, 0.5      # (B) P[0]=P[1]=1/2
P0_uc, P1_uc = 1/3, 2/3      # (C) P[0]=1/3, P[1]=2/3

# Q(x) 함수 (math.erfc는 스칼라 입력 → np.vectorize로 배열 지원)
def Q(x):
    return 0.5 * np.vectorize(math.erfc)(x / np.sqrt(2))

# 임계값 범위
tau = np.linspace(0, 1, 2001)
#균등 사전확률
Pe_eq = P0_eq * Q(tau / sigma) + P1_eq * Q((A - tau) / sigma)
tau_star_eq = A / 2  # 해석적 최적값 = 0.5

#비균등 사전확률
Pe_uc = P0_uc * Q(tau / sigma) + P1_uc * Q((A - tau) / sigma)
tau_star_uc = (sigma2 / A) * np.log(P0_uc / P1_uc) + A / 2  # 해석적 최적값
# 그래프
plt.figure(figsize=(7,5))
plt.plot(tau, Pe_eq, label="(B) Equal priors (P0=P1=0.5)", linewidth=2)
plt.plot(tau, Pe_uc, linestyle="--", label="(C) Unequal priors (P0=1/3, P1=2/3)", linewidth=2)
# 최적 임계값 위치에 수직선
plt.axvline(tau_star_eq, color="gray", linestyle=":", linewidth=1)
plt.axvline(tau_star_uc, color="gray", linestyle=":", linewidth=1)
plt.xlabel("Threshold")
plt.ylabel("Error Probability")
plt.title("3-(B) and 3-(C)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()