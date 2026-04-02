import matplotlib.pyplot as plt
import numpy as np
n_values = np.arange(1, 101)
num_trials = 10000

est_means = []
est_vars = []

for n in n_values:
    samples = np.random.randn(num_trials, n)

    Mn = np.mean(samples, axis=1)

    mean_of_Mn = np.mean(Mn)
    var_of_Mn = np.var(Mn)
    est_means.append(mean_of_Mn)
    est_vars.append(var_of_Mn)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(n_values, est_means, 'b-', label='Estimated Mean of $M_n$')
plt.axhline(y=0, color='r', linestyle='--', label='Original Mean (0)')
plt.title('Mean of Sample Mean ($M_n$)')
plt.xlabel('Sample Size (n)')
plt.ylabel('Mean')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(-0.1, 0.1)
plt.subplot(1, 2, 2)
plt.plot(n_values, est_vars, 'b-', label='Estimated Variance of $M_n$')
plt.plot(n_values, 1 / n_values, 'r--', label='Theoretical Variance ($1/n$)')
plt.axhline(y=1, color='g', linestyle=':', label='Original Variance (1)')
plt.title('Variance of Sample Mean ($M_n$)')
plt.xlabel('Sample Size (n)')
plt.ylabel('Variance')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()