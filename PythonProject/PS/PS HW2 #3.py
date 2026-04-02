import matplotlib.pyplot as plt
import numpy as np

max_rolls = 5000
target_number = 1
theory_prob = 1 / 6

rolls = np.random.randint(1, 7, size=max_rolls)

is_one = (rolls == target_number)
cum_counts = np.cumsum(is_one)
n_values = np.arange(1, max_rolls + 1)
rel_freq = cum_counts / n_values

plt.figure(figsize=(12, 6))
plt.plot(n_values, rel_freq, label='Relative Frequency', color='blue', linewidth=1)
plt.axhline(y=theory_prob, color='red', linestyle='--', linewidth=2, label='Theoretical Probability (1/6)')
plt.title('Law of Large Numbers (LLN) Verification', fontsize=14)
plt.xlabel('Number of Rolls (n)', fontsize=12)
plt.ylabel('Relative Frequency of rolling a "1"', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.ylim(0, 0.4)

plt.show()