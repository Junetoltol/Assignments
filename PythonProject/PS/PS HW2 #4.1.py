import matplotlib.pyplot as plt
import numpy as np
n_list = [1, 5, 30]  # 몇 개만 골라서 그림
trials = 100000

plt.figure(figsize=(12, 4))

for i, n in enumerate(n_list):
    X = np.random.randn(trials, n)
    M_n = X.mean(axis=1)

    # 이론 분포 N(0, 1/n)
    sigma = np.sqrt(1.0 / n)
    x = np.linspace(M_n.min(), M_n.max(), 200)
    const = 1 / (sigma * np.sqrt(2 * np.pi))
    y = const * np.exp(-0.5 * (x / sigma) ** 2)

    plt.subplot(1, len(n_list), i + 1)
    plt.hist(M_n, bins=40, density=True, alpha=0.6,
             color='skyblue', edgecolor='white', label='Simulation')
    plt.plot(x, y, 'r-', linewidth=2, label='N(0, 1/n) theory')

    plt.title(f'n = {n}')
    plt.xlabel('M_n')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)

plt.suptitle('Distribution of Sample Mean M_n for Standard Gaussian')
plt.tight_layout()
plt.show()
