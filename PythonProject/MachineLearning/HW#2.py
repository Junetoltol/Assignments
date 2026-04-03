import numpy as np

X = np.array([
    [1,  7,  560],
    [1,  3,  220],
    [1,  3,  340],
    [1,  4,   80],
    [1,  6,  150],
    [1,  7,  330],
    [1,  2,  110],
    [1,  7,  210],
    [1, 30, 1460],
    [1,  5,  605],
    [1, 16,  688],
    [1, 10,  215],
    [1,  4,  255],
    [1,  6,  462],
    [1,  9,  448],
    [1, 10,  776],
    [1,  6,  200],
    [1,  7,  132],
    [1,  3,   36],
    [1, 17,  770],
    [1, 10,  140],
    [1, 26,  810],
    [1,  9,  450],
    [1,  8,  635],
    [1,  4,  150]
], dtype=float)

y = np.array([
    16.68, 11.50, 12.03, 14.88, 13.75,
    18.11,  8.00, 17.83, 79.24, 21.50,
    40.33, 21.00, 13.50, 19.75, 24.00,
    29.00, 15.35, 19.00,  9.50, 35.10,
    17.90, 52.32, 18.75, 19.83, 10.75
], dtype=float)

def mle_linear_regression(X, y):
    return np.linalg.pinv(X.T @ X) @ X.T @ y

def map_linear_regression(X, y, alpha=1.0):
    # MAP regularization strength
    p = X.shape[1]
    I = np.eye(p)
    return np.linalg.pinv(X.T @ X + alpha * I) @ X.T @ y

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

w_mle = mle_linear_regression(X, y)
y_pred_mle = X @ w_mle
mse_mle = mse(y, y_pred_mle)

alpha = 1.0
w_map = map_linear_regression(X, y, alpha)
y_pred_map = X @ w_map
mse_map = mse(y, y_pred_map)

print("=== MLE ===")
print("w_mle =", w_mle)
print("MSE =", mse_mle)

print("\n=== MAP ===")
print("alpha =", alpha)
print("w_map =", w_map)
print("MSE =", mse_map)