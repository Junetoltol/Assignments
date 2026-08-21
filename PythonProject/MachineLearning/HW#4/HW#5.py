import numpy as np


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=float)

Y = np.array([
    [0],
    [1],
    [1],
    [0]
], dtype=float)


def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))


def sigmoid_derivative(a):
    return a * (1 - a)


def relu(z):
    return np.maximum(0, z)


def relu_derivative(z):
    return (z > 0).astype(float)


def binary_cross_entropy(y_true, y_pred):
    eps = 1e-12
    return -np.mean(
        y_true * np.log(y_pred + eps) +
        (1 - y_true) * np.log(1 - y_pred + eps)
    )


def train_xor(hidden_activation="relu",
              hidden_size=4,
              learning_rate=0.5,
              max_epochs=10000,
              target_loss=0.01,
              seed=42):

    np.random.seed(seed)

    input_size = 2
    output_size = 1

    if hidden_activation == "relu":
        W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2 / input_size)
    elif hidden_activation == "sigmoid":
        W1 = np.random.randn(input_size, hidden_size) * np.sqrt(1 / input_size)
    else:
        raise ValueError("hidden_activation must be 'relu' or 'sigmoid'")

    b1 = np.zeros((1, hidden_size))
    W2 = np.random.randn(hidden_size, output_size) * np.sqrt(1 / hidden_size)
    b2 = np.zeros((1, output_size))

    loss_history = []

    for epoch in range(1, max_epochs + 1):
        Z1 = np.dot(X, W1) + b1

        if hidden_activation == "relu":
            A1 = relu(Z1)
        else:
            A1 = sigmoid(Z1)

        Z2 = np.dot(A1, W2) + b2
        A2 = sigmoid(Z2)

        loss = binary_cross_entropy(Y, A2)
        loss_history.append(loss)

        predictions = (A2 >= 0.5).astype(int)
        accuracy = np.mean(predictions == Y)

        if accuracy == 1.0 and loss < target_loss:
            break

        m = X.shape[0]

        dZ2 = (A2 - Y) / m
        dW2 = np.dot(A1.T, dZ2)
        db2 = np.sum(dZ2, axis=0, keepdims=True)

        dA1 = np.dot(dZ2, W2.T)

        if hidden_activation == "relu":
            dZ1 = dA1 * relu_derivative(Z1)
        else:
            dZ1 = dA1 * sigmoid_derivative(A1)

        dW1 = np.dot(X.T, dZ1)
        db1 = np.sum(dZ1, axis=0, keepdims=True)

        W1 = W1 - learning_rate * dW1
        b1 = b1 - learning_rate * db1
        W2 = W2 - learning_rate * dW2
        b2 = b2 - learning_rate * db2

    result = {
        "activation": hidden_activation,
        "epoch": epoch,
        "loss": loss,
        "accuracy": accuracy,
        "W1": W1,
        "b1": b1,
        "W2": W2,
        "b2": b2,
        "predictions": predictions,
        "outputs": A2,
        "loss_history": loss_history
    }

    return result


def print_result(result):
    print("Hidden Layer Activation Function:", result["activation"])
    print("Converged Epoch:", result["epoch"])
    print("Final Loss:", round(result["loss"], 6))
    print("Final Accuracy:", result["accuracy"])

    print("\n[XOR Gate Test Result]")

    for x, output, pred, target in zip(X, result["outputs"], result["predictions"], Y):
        print(
            "Input:",
            x.astype(int),
            "Output Value:",
            round(float(output[0]), 6),
            "Predicted:",
            int(pred[0]),
            "Target:",
            int(target[0])
        )


def compare_results(relu_result, sigmoid_result):
    print("Convergence Performance Comparison")
    print("Activation\tEpoch\t\tFinal Loss\tAccuracy")
    print(
        "ReLU\t\t",
        relu_result["epoch"],
        "\t\t",
        round(relu_result["loss"], 6),
        "\t",
        relu_result["accuracy"]
    )
    print(
        "Sigmoid\t\t",
        sigmoid_result["epoch"],
        "\t\t",
        round(sigmoid_result["loss"], 6),
        "\t",
        sigmoid_result["accuracy"]
    )

if __name__ == "__main__":
    relu_result = train_xor(hidden_activation="relu")
    sigmoid_result = train_xor(hidden_activation="sigmoid")

    print_result(relu_result)
    print_result(sigmoid_result)

    compare_results(relu_result, sigmoid_result)