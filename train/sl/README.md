# 소개
5-layer Convolutional Neural Network를 사용해 특징 추출기로 사용하며, 지도 학습을 통해 학습함.  
지도 학습 데이터셋은 기존 SOTA 모델(N-Tuple network)의 플레이 기록을 사용하여 특정 상황에 어떤 방향으로 움직여야 하는 지 학습함.  

참고 논문 _Naoki Kondo, Kiminori Matsuzaki, Playing Game 2048 with Deep Convolutional Neural Networks Trained by Supervised Learning, Journal of Information Processing, 2019, Volume 27, Pages 340-347, Released on J-STAGE April 15, 2019, Online ISSN 1882-6652_  

<테스트 결과 (n_games=1000)>  
평균 점수: 30,733점  
최대 타일: 8192  
최고 점수: 177,072점  
