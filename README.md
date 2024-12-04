# **파이썬으로 Triple Triad 구현**

-20101235 박진우

## 1.게임에 대해

트리플 트라이어드(Triple Triad)의 규칙은 다음과 같습니다.

</u>**규칙**</u>

- 두 명의 플레이어가 있고 선공 플레이어는 5장, 후공 플레이어는 4장의 카드를 가진다.
- 3*3 보드에 각 플레이어가 번갈아가며 카드를 한 장씩 놓는다.
- 각 카드는 상/하/좌/우에 숫자가 쓰여 있고, 카드를 놓았을 때 인접한 카드 숫자를 비교해서 큰 쪽이 작은 쪽 카드를 지배할 수 있다. (내가 놓은 카드와 '인접한'  카드만이 영향을 받는다.)
- 나중에 배치한 내 카드가 인접한 상대 카드보다 작은 숫자라도 내 카드가 지배당하지는 않는다.
- 내가 배치한 카드와 인접한 상대 카드의 숫자가 같을 경우, 상대 카드 숫자 합과 내가 놓은 카드의 숫자 합을 비교하여 
큰 쪽이 지배한다. 합도 같다면 아무 일도 일어나지 않는다.
- 9장의 카드가 보드에 다 채워졌을 때, 더 많은 카드를 지배한 쪽이 승리한다. 단, 선공 플레이어의 지배를 받는 카드가 5장이고 후공 플레이어의 지배를 받는 카드가 4장이면 무승부이다.

상대 플레이어는 AI이고, 난이도에 따라 보드에 무작위 카드 배치를 하는 방법과 alpha-beta pruning을 이용한 방법을 다른 비율로 섞어 행동하도록 하였습니다.

매 게임마다 카드 덱은 무작위로 생성됩니다.

이미지는 카드의 경우 [](https://www.istockphoto.com/kr/%EB%B2%A1%ED%84%B0/%ED%94%8C%EB%A0%88%EC%9D%B4-%EC%B9%B4%EB%93%9C%EC%9D%98-%EB%B0%98%EB%8C%80%EC%AA%BD-gm1249328009-364073402)에서 가져와 가공하여 사용하였고, 나머지는 chatgpt를 활용하여 이미지를 얻은 후 가공하였습니다.

코드 중 Button class와 title 함수의 경우 [](https://github.com/kulord99/Othello)를 참고하였습니다.
나머지 부분은 chatgpt를 활용하였습니다.



## 2. 게임 시작 및 설정

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/title.png)

시작 화면에는 게임 시작 버튼이 있습니다. 

이 버튼을 누르면

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/difficulty.png)

난이도를 선택하는 화면이 나옵니다.
1번은 쉬움, 2번은 중간, 3번은 어려움 입니다.<br>
쉬움 난이도는 70% 확률로 무작위 배치를 하고 30% 확률로 alpha-beta pruning을 실행합니다.<br>
중간 난이도는 50% 확률로 무작위 배치를 하고 50% 확률로 alpha-beta pruning을 실행합니다.<br>
어려움 난이도는 30% 확률로 무작위 배치를 하고 70% 확률로 alpha-beta pruning을 실행합니다.<br>

그 다음에는 선공 여부를 선택하는 화면이 나옵니다.

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/turn.png)

1번은 선공, 2번은 후공 입니다.



## 3. 게임 플레이

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/play_1.png)

게임이 시작되었을 때 화면입니다. 위에는 점수가 표시되고, 그 아래에 보드가 있습니다.
맨 아래에 자신의 카드를 확인할 수 있습니다.

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/play_2.png)

좌우 방향키로 놓을 카드를 선택할 수 있고, 마우스로 보드의 자리를 클릭하여 해당 자리에 카드를 배치할 수 있습니다.

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/play_3.png)

게임이 끝나면 아래에 "Click the screen to see the result"가 출력되고 화면 아무 곳이나 클릭하면

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/result.png)

이처럼 결과가 표시되고 잠시 후

![image](https://github.com/jinwooapple/TripleTriad/blob/main/triple%20triad/image/markdown/retry_or_exit.png)

다시하거나 게임을 그대로 종료할 수 있는 화면이 나옵니다.
다시하기를 선택하면 시작 화면으로 돌아갑니다.
