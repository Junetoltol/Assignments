import numpy as np
import matplotlib.pyplot as plt

# 1) 시간축: -3π ~ 3π (여러 주기를 보고 싶어서 넓게)
T_min = -3*np.pi
T_max =  3*np.pi
num_points = 6000                  # 점 개수(크게 잡을수록 곡선이 매끈)
t = np.linspace(T_min, T_max, num_points)

# 2) 원래 신호(사각파): sgn(sin t) -> 값이 -1 또는 +1
x_original = np.sign(np.sin(t))

# 3) 푸리에 급수 근사
#    사각파는 홀수 고조파만 포함: x(t) ≈ (4/π) * sum_{k odd<=N} [ (1/k) sin(k t) ]
N_list = [5, 15, 51]               # 여러 N 값으로 비교 (필요시 추가/변경)
approxs = []                       # 나중에 분석/그래프용으로 보관

for N in N_list:
    y = np.zeros_like(t)
    for k in range(1, N+1, 2):     # 1,3,5,...,N (홀수만)
        y += (4/np.pi) * (1.0/k) * np.sin(k*t)
    approxs.append((N, y))

# 4) 전체 구간 플롯: 원신호 vs FS 근사 (여러 N)
plt.figure(figsize=(10, 6))
plt.plot(t, x_original, 'k', label='Original (square wave)')
for (N, y) in approxs:
    plt.plot(t, y, label=f'N={N}')
# 불연속(대략 t = mπ) 위치에 세로점선
for m in range(-3, 4):
    plt.axvline(m*np.pi, color='gray', lw=0.7, ls=':')
plt.title('Gibbs Phenomenon (Full Range)')
plt.xlabel('t'); plt.ylabel('x(t)')
plt.yticks([-1, 0, 1])
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 5) 불연속 근처 확대(요구사항 4번)
#    t=0 주변 작은 구간만 확대해서 보기 (예: -0.3 ~ 0.3)
zoom_half = 0.3
mask = (t >= -zoom_half) & (t <= zoom_half)
tz = t[mask]
xz = x_original[mask]

plt.figure(figsize=(10, 6))
plt.plot(tz, xz, 'k', label='Original (zoom)')
for (N, y) in approxs:
    plt.plot(tz, y[mask], label=f'N={N}')
# 기준선 표시 (사각파의 상/하단)
plt.axhline( 1, color='gray', lw=0.7, ls='--')
plt.axhline(-1, color='gray', lw=0.7, ls='--')
plt.title('Gibbs near t=0 (Zoomed)')
plt.xlabel('t'); plt.ylabel('x(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 6) 간단한 정량 확인(선택): overshoot/undershoot 근사치 출력
#    오른쪽(0+)에서 +1을 얼마나 넘는지, 왼쪽(0-)에서 -1을 얼마나 내려가는지
right_mask = (tz >= 0)
left_mask  = (tz <= 0)

print("=== Overshoot / Undershoot (near t=0) ===")
for (N, y_full) in approxs:
    yz = y_full[mask]
    # overshoot: 0+ 구간에서 (값 - 1)의 최대치
    overshoot = np.max(yz[right_mask] - 1.0)
    # undershoot: 0- 구간에서 (값 + 1)의 최소치 (음수일수록 더 내려감)
    undershoot = np.min(yz[left_mask] + 1.0)

    # 점프 크기(=2) 대비 퍼센트
    over_pct = 100.0 * max(0.0, overshoot) / 2.0
    under_pct = 100.0 * max(0.0, -undershoot) / 2.0

    print(f"N={N:3d} | overshoot ~ {overshoot: .4f}  ({over_pct: .2f} % of jump)")
    print(f"      | undershoot~ {undershoot: .4f}  ({under_pct: .2f} % of jump)")