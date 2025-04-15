# 감정 수집 게임

감정을 가진 귀여운 캐릭터들을 수집하고, 캐릭터와 교감하면서 성장시키는 웹 게임입니다.

## 기능

- 캐릭터 클래스 정의 (이름, 속성, 감정, 레벨, 경험치, 진화 레벨)
- 캐릭터 3종 샘플 생성 (피카츄, 꼬부기, 이상해씨)
- 캐릭터 리스트를 화면에 표 형식으로 출력
- 각 캐릭터와 교감하는 기능
  - 버튼 클릭 시 감정이 랜덤으로 바뀌고 경험치 +10
  - 경험치가 일정 수치 이상이면 레벨업
  - 레벨이 진화 레벨을 넘으면 "진화 완료!" 메시지 표시

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/사용자명/감정-수집-게임.git
cd 감정-수집-게임

# 필요한 패키지 설치
pip install -r requirements.txt

# 실행
streamlit run app.py
```

## 기술 스택

- Python 3.8+
- Streamlit
- Dataclasses

## 스크린샷

(스크린샷 추가 예정)

## 향후 계획

- 추가 캐릭터 및 속성 구현
- 캐릭터 이미지 추가
- 저장 기능 구현
- 캐릭터 상호작용 다양화

## 라이센스

MIT License 