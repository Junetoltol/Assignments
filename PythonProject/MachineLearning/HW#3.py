import numpy as np


'''
============================================================
[과제 기록]

문제:
    OR 게이트를 단층 퍼셉트론(perceptron)으로 구현한다.

학습 데이터:
    (0, 0) -> 0
    (0, 1) -> 1
    (1, 0) -> 1
    (1, 1) -> 1

OR 게이트의 의미:
    두 입력 x1, x2 중 하나라도 1이면 출력은 1이다.
    두 입력이 모두 0일 때만 출력은 0이다.

구현 조건:
    1. hard limiter activation 함수를 사용하여 구현한다.
    2. sigmoid activation 함수를 사용하여 구현한다.

기본 계산식:
    net = w1*x1 + w2*x2 + b
    y = activation(net)
    error = d - y

hard limiter 방식:
    hard limiter는 다음과 같이 정의된다.

        h(x) = 1, if x >= 0.5
        h(x) = 0, if x < 0.5

    hard limiter는 미분이 불가능하므로 일반적인 perceptron learning rule을 사용한다.

        w = w + learning_rate * error * x
        b = b + learning_rate * error

sigmoid 방식:
    sigmoid 함수는 다음과 같이 정의된다.

        sigmoid(x) = 1 / (1 + exp(-x))

    sigmoid 함수는 미분 가능하므로 gradient descent 방식으로 학습한다.
    sigmoid의 미분값은 y * (1 - y)이므로 delta를 다음과 같이 둔다.

        delta = (d - y) * y * (1 - y)

    그리고 weight와 bias를 다음과 같이 갱신한다.

        w = w + learning_rate * delta * x
        b = b + learning_rate * delta

목표:
    학습이 끝난 뒤 다음 결과가 나오면 OR 게이트 구현이 성공한 것이다.

        (0, 0) -> 0
        (0, 1) -> 1
        (1, 0) -> 1
        (1, 1) -> 1
============================================================
'''


'''
OR 게이트 학습 데이터
X는 입력 데이터이고, D는 각 입력에 대한 정답값이다.
'''
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=float)

D = np.array([0, 1, 1, 1], dtype=float)


def hard_limiter(net):
    '''
    Hard Limiter Activation Function

    문제에서 주어진 hard limiter 함수이다.

        h(x) = 1 if x >= 0.5
        h(x) = 0 if x < 0.5
    '''
    if net >= 0.5:
        return 1
    else:
        return 0


def train_hard_limiter(X, D, learning_rate=0.5, max_epochs=100):
    '''
    Hard Limiter를 이용한 퍼셉트론 학습 함수

    초기 가중치 w와 bias b는 0으로 설정한다.

    각 입력 x에 대하여 다음 과정을 반복한다.

        1. net = w1*x1 + w2*x2 + b 계산
        2. hard limiter를 적용하여 출력 y 계산
        3. error = d - y 계산
        4. perceptron learning rule로 weight와 bias 수정

    학습 규칙:

        w = w + learning_rate * error * x
        b = b + learning_rate * error

    한 epoch 동안 모든 데이터를 정확히 분류하면 학습을 종료한다.
    '''
    w = np.array([0.0, 0.0])
    b = 0.0

    for epoch in range(1, max_epochs + 1):
        error_count = 0

        for x, d in zip(X, D):
            net = np.dot(w, x) + b
            y = hard_limiter(net)

            error = d - y

            w = w + learning_rate * error * x
            b = b + learning_rate * error

            if error != 0:
                error_count += 1

        if error_count == 0:
            break

    return w, b, epoch


def sigmoid(net):
    '''
    Sigmoid Activation Function

    sigmoid 함수는 다음과 같이 정의된다.

        sigmoid(x) = 1 / (1 + exp(-x))

    출력값은 0과 1 사이의 실수값이다.
    최종 분류에서는 0.5 이상이면 1, 0.5 미만이면 0으로 판단한다.
    '''
    return 1 / (1 + np.exp(-net))


def train_sigmoid(X, D, learning_rate=0.5, max_epochs=10000):
    '''
    Sigmoid를 이용한 퍼셉트론 학습 함수

    sigmoid 함수는 미분 가능하므로 gradient descent 방식으로 학습한다.

    각 입력 x에 대하여 다음 과정을 반복한다.

        1. net = w1*x1 + w2*x2 + b 계산
        2. sigmoid(net)을 이용하여 출력 y 계산
        3. error = d - y 계산
        4. delta = (d - y) * y * (1 - y) 계산
        5. weight와 bias 수정

    sigmoid의 미분값:

        sigmoid'(x) = y * (1 - y)

    weight와 bias 갱신식:

        w = w + learning_rate * delta * x
        b = b + learning_rate * delta

    전체 오차가 충분히 작아지면 학습을 종료한다.
    '''
    w = np.array([0.0, 0.0])
    b = 0.0

    for epoch in range(1, max_epochs + 1):
        total_error = 0.0

        for x, d in zip(X, D):
            net = np.dot(w, x) + b
            y = sigmoid(net)

            delta = (d - y) * y * (1 - y)

            w = w + learning_rate * delta * x
            b = b + learning_rate * delta

            total_error += 0.5 * (d - y) ** 2

        if total_error < 0.001:
            break

    return w, b, epoch


def test_hard_limiter(w, b):
    '''
    Hard Limiter 방식으로 학습된 퍼셉트론을 테스트한다.

    각 입력에 대해 net 값을 계산하고,
    hard limiter를 적용한 최종 출력값을 확인한다.
    '''
    print("\n[Hard Limiter Perceptron Result]")
    print("Final weight:", w)
    print("Final bias:", b)

    for x in X:
        net = np.dot(w, x) + b
        y = hard_limiter(net)
        print(f"Input: {x.astype(int)}  Net: {net:.4f}  Output: {y}")


def test_sigmoid(w, b):
    '''
    Sigmoid 방식으로 학습된 퍼셉트론을 테스트한다.

    sigmoid 출력값은 0과 1 사이의 실수값이다.
    따라서 0.5 이상이면 1, 0.5 미만이면 0으로 최종 분류한다.
    '''
    print("\n[Sigmoid Perceptron Result]")
    print("Final weight:", w)
    print("Final bias:", b)

    for x in X:
        net = np.dot(w, x) + b
        y = sigmoid(net)
        y_class = 1 if y >= 0.5 else 0

        print(f"Input: {x.astype(int)}  Net: {net:.4f}  Sigmoid: {y:.4f}  Output: {y_class}")


if __name__ == "__main__":
    '''
    Main 실행 부분

    1. Hard limiter 방식으로 OR 게이트를 학습하고 테스트한다.
    2. Sigmoid 방식으로 OR 게이트를 학습하고 테스트한다.
    '''

    w_hard, b_hard, epoch_hard = train_hard_limiter(X, D)
    print("Hard Limiter training finished at epoch:", epoch_hard)
    test_hard_limiter(w_hard, b_hard)

    w_sigmoid, b_sigmoid, epoch_sigmoid = train_sigmoid(X, D)
    print("\nSigmoid training finished at epoch:", epoch_sigmoid)
    test_sigmoid(w_sigmoid, b_sigmoid)