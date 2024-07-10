## 💻 구현한 내용

- `python/numpy`를 이용해 시뮬레이션을 위한 2048 게임보드 및 알고리즘 구현
- CNN 기반 지도학습 구현을 위해 `pytorch` 사용

### 1. Expectimax search

- 트리 기반 적대적 탐색(minimax search) 알고리즘
- 플레이어는 점수 최대화, 컴퓨터는 점수 최소화를 목적으로 함
    - 플레이어는 매 step마다 새로운 타일이 놓일 상태를 고려하여 최적의 행동을 선택함
    - action을 취할 때마다 바뀐 state가 트리의 자식 노드로 생성됨
    - `max`와 `expect`가 재귀적으로 차례로 호출됨 (max depth에 도달하거나 게임종료될때까지)

### 2. 논문구현: TD-Afterstate + N-Tuple network

- *Szubert, et al., "Temporal difference learning of n-tuple networks for the game 2048." IEEE Conf. Comput. Intel. Games, 2014.* [논문 요약 블로그 포스팅](https://velog.io/@jmnsb/Paper-Review-Temporal-Difference-Learning-of-N-Tuple-Networks-for-the-Game-2048)
- N-Tuple network를 이용해 2048 게임 보드에 대한 state value 평가
- Temporal difference learning을 이용해 state value function 학습

### 3. 논문구현: CNN 특징추출 + 지도학습

- *Kondo & Matsuzaki, “Playing Game 2048 with Deep Convolutional Neural Networks Trained by Supervised Learning”, J. Info. Process., 2019*
- 2048 게임 보드를 4x4의 이미지로 취급하여 DCNN으로 특징 추출
- 기존 SOTA 모델(e.g. N-tuple net)의 플레이 기록을 학습데이터로 사용하여 매 state별 action을 지도 학습함
