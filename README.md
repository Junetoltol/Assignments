<div align="center">

# University Coursework Archive

정보통신공학 학부 과정에서 구현하고 실험한 내용을 정리한 저장소입니다.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-Data%20Structures-ED8B00?logo=openjdk&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-IoT-C51A4A?logo=raspberrypi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy&logoColor=white)

</div>

## About this repository

단순 제출물 보관을 넘어, 수업에서 배운 개념을 어떤 코드와 실험으로 확인했는지 한눈에 볼 수 있도록 정리했습니다. IoT 하드웨어 제어부터 머신러닝 기초 구현, 알고리즘, 확률·신호 처리, 자료구조까지 학습 흐름을 담고 있습니다.

> 이 저장소의 코드는 학습·실습 목적입니다. 일부 파일은 수업에서 제공된 구조나 예제를 바탕으로 확장했으며, 상용 환경을 위한 완성형 라이브러리가 아닙니다.

## What I worked on

| Area | Topics and implementations | Evidence |
| --- | --- | --- |
| **IoT & Embedded Systems** | Raspberry Pi GPIO, PIR·DHT11·초음파 센서, I2C LCD, 부저, 카메라 기반 색상 판별, Azure IoT Hub 텔레메트리 | [IoTSystemAssistant](./IoTSystemAssistant), [IoT system practice](./IotSystem-main) |
| **Machine Learning** | 선형회귀 MLE/MAP, Hard Limiter·Sigmoid 학습, XOR 분류, NumPy 기반 3·4계층 신경망과 MNIST 분류 | [MachineLearning](./PythonProject/MachineLearning) |
| **Algorithms & Information Theory** | Greedy scheduling, 중복 탐색, Kadane 알고리즘, 최대합 부분행렬, Huffman coding | [Algorithm](./PythonProject/Algorithm) |
| **Probability & Statistics** | 역변환 표본 생성, 경험적 CDF, 검출 임계값, 중심극한정리와 대수의 법칙 시뮬레이션 | [Probability exercises](./PythonProject/PS) |
| **Signals & Systems** | Fourier series, Gibbs phenomenon, CTFT·DTFT, sampling과 aliasing 시각화 | [Signals exercises](./PythonProject/SS) |
| **Data Structures** | Stack·Queue, tree traversal, binary search tree, heap, graph traversal | [Java assignments](./Java_Data_Structure_assignment) |

## Selected highlights

### 1. Camera color detection with physical feedback

Raspberry Pi 카메라로 이미지를 촬영하고 중앙 ROI를 HSV 색공간에서 분석합니다. 대표 색상을 I2C LCD에 표시하고 지정 색상이 감지되면 GPIO 부저를 울리도록 연결했습니다.

- [색상 비율 분석](./IoTSystemAssistant/color_detect.py)
- [LCD·부저 통합](./IoTSystemAssistant/color_lcd_buzzer.py)
- 핵심 기술: `OpenCV`, `NumPy`, `rpicam-still`, `GPIO`, `I2C`

### 2. Sensor telemetry to Azure IoT Hub

진동 센서 이벤트를 감지해 누적 횟수와 시각을 JSON 메시지로 만들고 Azure IoT Hub에 전송하는 흐름을 구현했습니다. 연결 문자열은 코드에 저장하지 않고 환경 변수로 주입합니다.

- [Azure IoT 전송 코드](<./IoTSystemAssistant/IOT%20AZURE.py>)
- 핵심 기술: `RPi.GPIO`, `azure-iot-device`, JSON telemetry

### 3. Neural networks built with NumPy

라이브러리의 고수준 학습 API에 의존하지 않고 forward propagation, loss, gradient 계산과 parameter update 흐름을 코드로 확인하고 확장했습니다. 3계층·4계층 구조를 같은 MNIST 조건에서 학습하도록 구현했습니다.

- [3·4계층 신경망](./PythonProject/MachineLearning/HW%234/HW%234.py)
- [XOR 활성화 함수 비교](./PythonProject/MachineLearning/HW%234/HW%235.py)
- 핵심 기술: `NumPy`, `Matplotlib`, backpropagation, mini-batch learning

### 4. Algorithms from problem to implementation

문제 조건에 맞춰 greedy scheduling, 1D·2D maximum subarray, duplicate detection, Huffman coding을 Python으로 구현했습니다.

- [Algorithm assignments](./PythonProject/Algorithm)
- [Huffman coding](./PythonProject/Algorithm/정보이론_HW%233_최은준.py)

## Repository structure

```text
Assignments/
├── IoTSystemAssistant/              # Raspberry Pi 센서·카메라·Azure 연동
├── IotSystem-main/                  # IoT 시스템 실습과 C/Python 코드
├── Java_Data_Structure_assignment/  # Java 자료구조 구현
└── PythonProject/
    ├── Algorithm/                   # 알고리즘·정보이론
    ├── MachineLearning/             # 회귀·퍼셉트론·신경망
    ├── PS/                          # 확률·통계 시뮬레이션
    └── SS/                          # 신호 및 시스템
```

## Running the code

각 폴더의 코드는 서로 다른 수업 환경과 하드웨어를 대상으로 합니다.

- Raspberry Pi 코드는 GPIO 핀 배치, 연결 센서, I2C 주소를 먼저 확인해야 합니다.
- 머신러닝·확률·신호 실험은 주로 `numpy`와 `matplotlib`를 사용합니다.
- MNIST 원본 데이터와 생성된 캐시는 저장소에 포함하지 않습니다. 실행 전 데이터 로더가 요구하는 파일을 별도로 준비해야 합니다.
- Azure 연결 문자열과 API 키 같은 인증정보는 환경 변수로만 전달합니다. `.env.example`에는 변수 이름만 기록합니다.

## Notes

- 제출 당시의 학습 과정을 보존하기 위해 과제별 파일 구조와 구현 스타일은 대부분 유지했습니다.
- 생성 파일, IDE 설정, 캐시, 다운로드 데이터와 인증정보는 버전 관리에서 제외합니다.
- 코드별 배경과 실험 결과는 대표 항목부터 점진적으로 문서화할 예정입니다.
