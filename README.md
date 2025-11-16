# 📰 네이버 뉴스 AI 요약 서비스

네이버 뉴스 검색 API와 OpenAI GPT를 활용하여 뉴스를 자동으로 한 문장 요약해주는 웹 서비스입니다.

## 🎯 주요 기능

- 🔍 네이버 뉴스 실시간 검색
- 🤖 OpenAI GPT-4o-mini 기반 한 문장 요약
- 📱 모바일 반응형 UI
- 🎨 깔끔한 카드형 디자인

## 🛠️ 기술 스택

- **Backend**: Flask (Python)
- **API**: Naver Search API, OpenAI API
- **Frontend**: HTML5, CSS3

## 📋 설치 방법

### 1. 저장소 클론 또는 다운로드

### 2. 가상환경 생성 및 활성화 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env` 파일에 본인의 API 키를 입력하세요:

```env
CLIENT_ID=your_naver_client_id
CLIENT_SECRET=your_naver_client_secret
OPENAI_KEY=your_openai_api_key
```

**API 키 발급 방법:**
- 네이버 API: https://developers.naver.com/
- OpenAI API: https://platform.openai.com/

### 5. 서버 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 📁 프로젝트 구조

```
네이버 뉴스 서비스/
│
├── app.py              # Flask 메인 애플리케이션
├── templates/          # HTML 템플릿
│   ├── home.html       # 홈페이지
│   └── results.html    # 검색 결과 페이지
├── static/             # 정적 파일
│   └── style.css       # 스타일시트
├── .env                # 환경변수 (API 키)
├── .gitignore          # Git 무시 파일
├── requirements.txt    # Python 패키지 목록
└── README.md           # 프로젝트 설명
```

## 🎨 화면 구성

### 1️⃣ 홈 페이지 (/)
- 검색창과 서비스 설명
- 키워드 입력 및 검색

### 2️⃣ 결과 페이지 (/search)
- 뉴스 카드 리스트
- 원문 미리보기
- AI 요약 문장
- 기사 링크

## 🚀 사용 방법

1. 홈페이지에서 관심있는 키워드 입력 (예: "AI", "경제", "날씨")
2. 검색 버튼 클릭
3. 네이버에서 관련 뉴스 5개 수집
4. GPT가 각 뉴스를 한 문장으로 요약
5. 카드 형태로 결과 확인
6. "전체 기사 보기" 클릭 시 원문 확인

## ⚠️ 주의사항

- `.env` 파일은 절대 Git에 커밋하지 마세요
- API 키는 개인정보이므로 공개하지 마세요
- OpenAI API 사용량에 따라 과금될 수 있습니다

## 📝 라이선스

MIT License

## 👨‍💻 개발자

- 종익님의 스터디 프로젝트

