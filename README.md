# 지뢰 찾기 모험 게임
블록을 제거해가며 길을 개척해 열쇠를 획득하고 목적지로 도착하면 성공!

- 마우스로 클릭하거나 스페이스 바를 눌러 블록 제거
- 주변에 지뢰가 없을 경우 지뢰가 있는 블록까지 블록이 한 번에 사라짐
- 마우스 우클릭을 하거나 F 키를 눌러 깃발로 지뢰의 위치 표시 가능
- 마우스 아이템을 통해 맞닿아 있지 않는 블록 오픈 가능
- 한 게임당 기회는 3번, 하트 아이템을 통해 1번의 추가 기회를 얻을 수 있음
  
### 게임 룰
![image](https://github.com/user-attachments/assets/cfc57b51-cfe0-41a9-85da-4995941251db)

### 게임 진행 화면
![image](https://github.com/user-attachments/assets/2e0f4276-712a-4728-94fc-142f0bd6f36c)

### 게임 종료 화면
![image](https://github.com/user-attachments/assets/98ec76ed-ae66-45fb-94ea-83f6fa2c9ccc)

### 사용된 컴퓨팅 사고 기법
- 분해
  - 주변 지뢰의 개수 반환 함수
  - 키보드의 방향 키를 통한 캐릭터의 이동
  - 마우스 왼쪽 클릭, 스페이스바를 통해 블록 오픈
  - 마우스 오른쪽 클릭, F키를 통해 지뢰 표시
  - 지뢰나 아이템을 눌렀을 때 발생하는 일
  - 게임에 성공하거나 실패했을 때 발생하는 일
- 패턴인식
  - for문을 사용하여 배경 블록 설치
  - 랜덤 모듈을 사용해 지뢰아 아이템 설치
- 추상화
  - 메인 루프의 변수 filed, xpos, ypos를 매개화하여 블록을 여는 함수 선언
- 알고리즘
  - 랜덤으로 지뢰와 아이템 설치
  - 캐릭터를 이동해가며 블록 오픈
    - 비어있는 칸을 누르면 블록 오픈
    - 생명 아이템이 있으면 목숨이 하나 추가되고 점수 +200
    - 마우스 아이템이 있으면 먼 곳에 있는 블록을 열 수 있는 기회가 생기고 점수 +200
    - 지뢰가 있으면 목숨이 하나 감소하고 점수 -100
  - 목숨이 0이 되거나 열쇠 아이템을 획득했고, 목적지에 도달하면 게임 종료
  - 소요 시간과 점수 띄우기
  - F5키를 통해 게임 재시작

### 팀원
|김지수|박수연|이다영|이승윤|
|------|------|------|------|
