# OpenAI 채팅 어시스턴트

Streamlit과 OpenAI API를 사용한 간단한 채팅 어시스턴트 프로토타입입니다.

## 설치 방법

1. 저장소를 클론합니다:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

3. `.env` 파일에 OpenAI API 키를 입력합니다:

```
OPENAI_API_KEY=your_api_key_here
```

## 실행 방법

다음 명령어로 애플리케이션을 실행합니다:

```bash
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501`이 열립니다.

## 주요 기능

- OpenAI의 GPT 모델을 사용한 대화형 인터페이스
- 스트리밍 응답으로 실시간 답변 확인
- 대화 기록 유지
- 직관적인 UI와 사용 안내

## 참고사항

이 앱은 프로토타입이며, 실제 서비스에 사용하기 전에 보안 및 오류 처리 등을 강화해야 합니다.
