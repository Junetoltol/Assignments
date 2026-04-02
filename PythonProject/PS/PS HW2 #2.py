import matplotlib.pyplot as plt
import numpy as np

n_list = [1, 2, 10, 30]
trials = 100000


mu_die = 3.5
var_die = 35 / 12

plt.figure(figsize=(12, 10))

for i in range(len(n_list)):
    n = n_list[i]
    dice = np.random.randint(1, 7, size=(trials, n))
    Sn = np.sum(dice, axis=1)
    mu_Sn = n * mu_die
    sigma_Sn = np.sqrt(n * var_die)
    x = np.linspace(min(Sn), max(Sn), 100)
    const = 1 / (sigma_Sn * np.sqrt(2 * np.pi))
    exp_part = np.exp(-0.5 * ((x - mu_Sn) / sigma_Sn) ** 2)
    y = const * exp_part

    plt.subplot(2, 2, i + 1)

    plt.hist(Sn, bins=30, density=True, color='skyblue', edgecolor='white', label='Simulation')

    plt.plot(x, y, 'r-', linewidth=2, label='Theory (CLT)')

    plt.title(f'n = {n}')
    plt.xlabel('Sum (Sn)')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(True, alpha=0.3)

plt.suptitle('CLT Verification: Sum of n Dice Rolls')
plt.tight_layout()
plt.show()