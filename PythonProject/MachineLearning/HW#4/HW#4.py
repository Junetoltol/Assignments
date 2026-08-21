# ============================================================
# HW #4: 3-layer and 4-layer Neural Network 구현
# MNIST 손글씨 숫자 분류
#
# 준비물:
#   - 이 파일과 같은 폴더에 mnist.py가 있어야 한다.
#   - 이 파일과 같은 폴더에 MNIST 압축 파일 4개가 있어야 한다.
#       train-images-idx3-ubyte.gz
#       train-labels-idx1-ubyte.gz
#       t10k-images-idx3-ubyte.gz
#       t10k-labels-idx1-ubyte.gz
#
# 교수님이 올려주신 TwoNN_Python.ipynb 구조를 확장한 코드입니다.
# TwoLayerNet: 입력층 -> 은닉층1 -> 출력층
# ThreeLayerNet: 입력층 -> 은닉층1 -> 은닉층2 -> 출력층
# FourLayerNet: 입력층 -> 은닉층1 -> 은닉층2 -> 은닉층3 -> 출력층
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from mnist import load_mnist


# ------------------------------------------------------------
# 1. 활성화 함수와 손실 함수
# ------------------------------------------------------------
def sigmoid(x):
    """Sigmoid activation function"""
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    """Sigmoid derivative"""
    return sigmoid(x) * (1.0 - sigmoid(x))


def softmax(x):
    """Softmax function with overflow prevention"""
    if x.ndim == 2:
        x = x - np.max(x, axis=1, keepdims=True)
        return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

    x = x - np.max(x)
    return np.exp(x) / np.sum(np.exp(x))


def cross_entropy_error(y, t):
    """Cross entropy loss"""
    if y.ndim == 1:
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)

    # t가 one-hot이 아니라 정수 레이블인 경우도 처리
    if t.size == y.size:
        t = t.argmax(axis=1)

    batch_size = y.shape[0]
    delta = 1e-7
    return -np.sum(np.log(y[np.arange(batch_size), t] + delta)) / batch_size


# ------------------------------------------------------------
# 2. 3-Layer Neural Network
#    입력층 -> 은닉층1 -> 은닉층2 -> 출력층
# ------------------------------------------------------------
class ThreeLayerNet:
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size,
                 weight_init_std=0.01):
        self.params = {}

        # W1: 입력층 784개 -> 은닉층1
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size1)
        self.params['b1'] = np.zeros(hidden_size1)

        # W2: 은닉층1 -> 은닉층2
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size1, hidden_size2)
        self.params['b2'] = np.zeros(hidden_size2)

        # W3: 은닉층2 -> 출력층 10개
        self.params['W3'] = weight_init_std * np.random.randn(hidden_size2, output_size)
        self.params['b3'] = np.zeros(output_size)

    def predict(self, x):
        W1, W2, W3 = self.params['W1'], self.params['W2'], self.params['W3']
        b1, b2, b3 = self.params['b1'], self.params['b2'], self.params['b3']

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)

        a2 = np.dot(z1, W2) + b2
        z2 = sigmoid(a2)

        a3 = np.dot(z2, W3) + b3
        y = softmax(a3)

        return y

    def loss(self, x, t):
        y = self.predict(x)
        return cross_entropy_error(y, t)

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)

        if t.ndim != 1:
            t = np.argmax(t, axis=1)

        return np.sum(y == t) / float(x.shape[0])

    def gradient(self, x, t):
        W1, W2, W3 = self.params['W1'], self.params['W2'], self.params['W3']
        b1, b2, b3 = self.params['b1'], self.params['b2'], self.params['b3']
        grads = {}
        batch_num = x.shape[0]

        # -------------------- forward --------------------
        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)

        a2 = np.dot(z1, W2) + b2
        z2 = sigmoid(a2)

        a3 = np.dot(z2, W3) + b3
        y = softmax(a3)

        # -------------------- backward --------------------
        # softmax + cross entropy의 미분
        dy = (y - t) / batch_num

        # 출력층 W3, b3 기울기
        grads['W3'] = np.dot(z2.T, dy)
        grads['b3'] = np.sum(dy, axis=0)

        # 은닉층2로 오차 역전파
        da2 = np.dot(dy, W3.T)
        dz2 = sigmoid_grad(a2) * da2
        grads['W2'] = np.dot(z1.T, dz2)
        grads['b2'] = np.sum(dz2, axis=0)

        # 은닉층1로 오차 역전파
        da1 = np.dot(dz2, W2.T)
        dz1 = sigmoid_grad(a1) * da1
        grads['W1'] = np.dot(x.T, dz1)
        grads['b1'] = np.sum(dz1, axis=0)

        return grads


# ------------------------------------------------------------
# 3. 4-Layer Neural Network
#    입력층 -> 은닉층1 -> 은닉층2 -> 은닉층3 -> 출력층
# ------------------------------------------------------------
class FourLayerNet:
    def __init__(self, input_size, hidden_size1, hidden_size2, hidden_size3, output_size,
                 weight_init_std=0.01):
        self.params = {}

        # W1: 입력층 784개 -> 은닉층1
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size1)
        self.params['b1'] = np.zeros(hidden_size1)

        # W2: 은닉층1 -> 은닉층2
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size1, hidden_size2)
        self.params['b2'] = np.zeros(hidden_size2)

        # W3: 은닉층2 -> 은닉층3
        self.params['W3'] = weight_init_std * np.random.randn(hidden_size2, hidden_size3)
        self.params['b3'] = np.zeros(hidden_size3)

        # W4: 은닉층3 -> 출력층 10개
        self.params['W4'] = weight_init_std * np.random.randn(hidden_size3, output_size)
        self.params['b4'] = np.zeros(output_size)

    def predict(self, x):
        W1, W2, W3, W4 = self.params['W1'], self.params['W2'], self.params['W3'], self.params['W4']
        b1, b2, b3, b4 = self.params['b1'], self.params['b2'], self.params['b3'], self.params['b4']

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)

        a2 = np.dot(z1, W2) + b2
        z2 = sigmoid(a2)

        a3 = np.dot(z2, W3) + b3
        z3 = sigmoid(a3)

        a4 = np.dot(z3, W4) + b4
        y = softmax(a4)

        return y

    def loss(self, x, t):
        y = self.predict(x)
        return cross_entropy_error(y, t)

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)

        if t.ndim != 1:
            t = np.argmax(t, axis=1)

        return np.sum(y == t) / float(x.shape[0])

    def gradient(self, x, t):
        W1, W2, W3, W4 = self.params['W1'], self.params['W2'], self.params['W3'], self.params['W4']
        b1, b2, b3, b4 = self.params['b1'], self.params['b2'], self.params['b3'], self.params['b4']
        grads = {}
        batch_num = x.shape[0]

        # -------------------- forward --------------------
        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)

        a2 = np.dot(z1, W2) + b2
        z2 = sigmoid(a2)

        a3 = np.dot(z2, W3) + b3
        z3 = sigmoid(a3)

        a4 = np.dot(z3, W4) + b4
        y = softmax(a4)

        # -------------------- backward --------------------
        # softmax + cross entropy의 미분
        dy = (y - t) / batch_num

        # 출력층 W4, b4 기울기
        grads['W4'] = np.dot(z3.T, dy)
        grads['b4'] = np.sum(dy, axis=0)

        # 은닉층3으로 오차 역전파
        da3 = np.dot(dy, W4.T)
        dz3 = sigmoid_grad(a3) * da3
        grads['W3'] = np.dot(z2.T, dz3)
        grads['b3'] = np.sum(dz3, axis=0)

        # 은닉층2로 오차 역전파
        da2 = np.dot(dz3, W3.T)
        dz2 = sigmoid_grad(a2) * da2
        grads['W2'] = np.dot(z1.T, dz2)
        grads['b2'] = np.sum(dz2, axis=0)

        # 은닉층1로 오차 역전파
        da1 = np.dot(dz2, W2.T)
        dz1 = sigmoid_grad(a1) * da1
        grads['W1'] = np.dot(x.T, dz1)
        grads['b1'] = np.sum(dz1, axis=0)

        return grads


# ------------------------------------------------------------
# 4. 학습 함수
# ------------------------------------------------------------
def train_network(network, x_train, t_train, x_test, t_test,
                  iters_num=10000, batch_size=100, learning_rate=0.1,
                  title='Neural Network'):
    train_size = x_train.shape[0]
    iter_per_epoch = max(train_size // batch_size, 1)

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    print('\n============================================================')
    print(title, 'training start')
    print('============================================================')

    for i in range(iters_num):
        # 미니배치 획득
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        # 기울기 계산: back propagation 사용
        grad = network.gradient(x_batch, t_batch)

        # 매개변수 갱신
        for key in network.params.keys():
            network.params[key] -= learning_rate * grad[key]

        # 손실값 기록
        loss = network.loss(x_batch, t_batch)
        train_loss_list.append(loss)

        # 1 epoch마다 정확도 출력
        if i % iter_per_epoch == 0:
            train_acc = network.accuracy(x_train, t_train)
            test_acc = network.accuracy(x_test, t_test)
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            print('i =', i,
                  '| train acc =', round(train_acc, 4),
                  '| test acc =', round(test_acc, 4),
                  '| loss =', round(loss, 4))

    print(title, 'training finished')

    # 정확도 그래프
    x = np.arange(len(train_acc_list))
    plt.figure()
    plt.plot(x, train_acc_list, label='train acc')
    plt.plot(x, test_acc_list, label='test acc', linestyle='--')
    plt.xlabel('epochs')
    plt.ylabel('accuracy')
    plt.ylim(0, 1.0)
    plt.title(title)
    plt.legend(loc='lower right')
    plt.show()

    return train_loss_list, train_acc_list, test_acc_list


# ------------------------------------------------------------
# 5. 메인 실행부
# ------------------------------------------------------------
if __name__ == '__main__':
    # 결과 재현용. 매번 다른 결과를 원하면 이 줄을 지워도 됨.
    np.random.seed(0)

    # MNIST 데이터 읽기
    # flatten=True: 28x28 이미지를 784차원 벡터로 변환
    # normalize=True: 픽셀값을 0~1 사이로 정규화
    # one_hot_label=True: 정답을 one-hot 벡터로 변환
    (x_train, t_train), (x_test, t_test) = load_mnist(
        flatten=True,
        normalize=True,
        one_hot_label=True
    )

    print('x_train:', x_train.shape)
    print('t_train:', t_train.shape)
    print('x_test :', x_test.shape)
    print('t_test :', t_test.shape)

    # --------------------------------------------------------
    # 3-layer neural net 학습
    # --------------------------------------------------------
    three_network = ThreeLayerNet(
        input_size=784,
        hidden_size1=50,
        hidden_size2=50,
        output_size=10
    )

    three_train_loss, three_train_acc, three_test_acc = train_network(
        network=three_network,
        x_train=x_train,
        t_train=t_train,
        x_test=x_test,
        t_test=t_test,
        iters_num=10000,
        batch_size=100,
        learning_rate=0.1,
        title='ThreeLayerNet'
    )

    # --------------------------------------------------------
    # 4-layer neural net 학습
    # --------------------------------------------------------
    four_network = FourLayerNet(
        input_size=784,
        hidden_size1=50,
        hidden_size2=50,
        hidden_size3=50,
        output_size=10
    )

    four_train_loss, four_train_acc, four_test_acc = train_network(
        network=four_network,
        x_train=x_train,
        t_train=t_train,
        x_test=x_test,
        t_test=t_test,
        iters_num=10000,
        batch_size=100,
        learning_rate=0.1,
        title='FourLayerNet'
    )

    # --------------------------------------------------------
    # 샘플 하나 예측 확인
    # --------------------------------------------------------
    id_test = 5
    img = x_test[id_test]
    label = np.argmax(t_test[id_test])

    three_out = three_network.predict(img)
    four_out = four_network.predict(img)

    print('\nSample test id:', id_test)
    print('Real label:', label)
    print('ThreeLayerNet prediction:', np.argmax(three_out))
    print('FourLayerNet prediction :', np.argmax(four_out))