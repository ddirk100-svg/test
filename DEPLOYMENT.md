# 🚀 네이버 뉴스 AI 요약 서비스 배포 가이드

이 문서는 Flask 앱을 외부에 배포하는 방법을 설명합니다.

---

## 📋 배포 전 준비사항

### 1. GitHub 저장소 생성

배포하기 전에 코드를 GitHub에 업로드해야 합니다.

#### 방법 1: GitHub Desktop 사용 (초보자 추천)
1. [GitHub Desktop](https://desktop.github.com/) 다운로드
2. GitHub 계정으로 로그인
3. File → Add local repository → 프로젝트 폴더 선택
4. Publish repository 클릭

#### 방법 2: Git 명령어 사용
```bash
# Git 초기화
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit"

# GitHub에 저장소 생성 후
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

---

## 🎯 방법 1: Render로 배포 (⭐ 가장 추천!)

### 장점
- ✅ 완전 무료
- ✅ 설정 매우 간단
- ✅ HTTPS 자동 제공
- ✅ 자동 배포 (GitHub 푸시 시)

### 단계별 가이드

#### 1단계: Render 회원가입
1. [Render.com](https://render.com/) 접속
2. GitHub 계정으로 가입

#### 2단계: 새 웹 서비스 생성
1. Dashboard → **New +** 버튼 클릭
2. **Web Service** 선택
3. GitHub 저장소 연결
4. 프로젝트 저장소 선택

#### 3단계: 설정
```
Name: naver-news-summary (원하는 이름)
Region: Singapore (가장 가까운 지역)
Branch: main
Root Directory: (비워두기)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free
```

#### 4단계: 환경변수 설정
**Environment Variables** 섹션에서 추가:
```
CLIENT_ID = your_naver_client_id
CLIENT_SECRET = your_naver_client_secret
OPENAI_KEY = your_openai_api_key
```

#### 5단계: 배포
**Create Web Service** 클릭!

🎉 완료! 5-10분 후 `https://your-app-name.onrender.com`에서 접속 가능!

---

## 🐍 방법 2: PythonAnywhere로 배포

### 장점
- ✅ Python 전용 호스팅
- ✅ 무료 티어 제공
- ⚠️ 무료는 외부 API 제한 있음 (화이트리스트 필요)

### 단계별 가이드

#### 1단계: 회원가입
1. [PythonAnywhere.com](https://www.pythonanywhere.com/) 접속
2. 무료 계정 생성

#### 2단계: 코드 업로드
1. Dashboard → **Files** 탭
2. 새 디렉토리 생성: `naver-news`
3. 모든 파일 업로드 (app.py, templates, static, etc.)

#### 3단계: 가상환경 생성
**Bash Console** 열기:
```bash
cd naver-news
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4단계: Web App 설정
1. **Web** 탭 → **Add a new web app**
2. Flask 선택
3. Python 3.10 선택
4. Path 설정: `/home/yourusername/naver-news/app.py`

#### 5단계: WSGI 파일 수정
WSGI configuration file 편집:
```python
import sys
path = '/home/yourusername/naver-news'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

#### 6단계: 환경변수 설정
**Files** 탭에서 `.env` 파일 생성

#### 7단계: 재시작
**Reload** 버튼 클릭!

🎉 완료! `https://yourusername.pythonanywhere.com`에서 접속 가능!

⚠️ **주의**: 무료 계정은 외부 API 호출에 제한이 있습니다. 네이버와 OpenAI API를 화이트리스트에 추가해야 합니다.

---

## 🚂 방법 3: Railway로 배포

### 장점
- ✅ 설정 매우 간단
- ✅ $5 무료 크레딧
- ⚠️ 크레딧 소진 시 유료

### 단계별 가이드

#### 1단계: Railway 회원가입
1. [Railway.app](https://railway.app/) 접속
2. GitHub 계정으로 가입

#### 2단계: 프로젝트 생성
1. **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. 저장소 선택

#### 3단계: 환경변수 설정
**Variables** 탭에서 추가:
```
CLIENT_ID = ...
CLIENT_SECRET = ...
OPENAI_KEY = ...
```

#### 4단계: 배포
자동으로 배포됩니다!

🎉 완료! Railway가 제공하는 URL로 접속 가능!

---

## 🔧 배포 후 체크리스트

- [ ] 홈페이지 접속 확인
- [ ] 검색 기능 테스트
- [ ] AI 요약 작동 확인
- [ ] 모바일 반응형 확인
- [ ] HTTPS 적용 확인

---

## 🐛 문제 해결

### 문제 1: 500 Internal Server Error
- **원인**: 환경변수 미설정
- **해결**: `.env` 파일 또는 플랫폼 환경변수 확인

### 문제 2: Module not found
- **원인**: requirements.txt 미설치
- **해결**: 빌드 로그 확인, gunicorn 추가

### 문제 3: Timeout Error
- **원인**: OpenAI API 응답 지연
- **해결**: 타임아웃 설정 증가 또는 비동기 처리

---

## 💰 비용 비교

| 플랫폼 | 무료 티어 | 제한사항 | 추천도 |
|--------|----------|----------|--------|
| **Render** | ✅ 영구 무료 | 15분 비활성 시 슬립 | ⭐⭐⭐⭐⭐ |
| **PythonAnywhere** | ✅ 무료 | 외부 API 제한 | ⭐⭐⭐ |
| **Railway** | $5 크레딧 | 크레딧 소진 시 유료 | ⭐⭐⭐⭐ |
| **Vercel** | ✅ 무료 | Serverless (Flask 비추천) | ⭐⭐ |
| **Heroku** | ❌ 유료 전환 | 최소 $7/월 | ⭐ |

---

## 🎯 추천 순서

### 초보자
1. **Render** (가장 쉬움)
2. Railway
3. PythonAnywhere

### 무료 호스팅 필요
1. **Render** (영구 무료)
2. PythonAnywhere (제한 있음)

### 빠른 배포
1. **Railway** (1분 배포)
2. Render

---

## 📚 추가 학습 자료

- [Render 공식 문서](https://render.com/docs)
- [PythonAnywhere 튜토리얼](https://help.pythonanywhere.com/pages/Flask/)
- [Railway 가이드](https://docs.railway.app/)

---

## 🆘 도움이 필요하면?

배포 중 문제가 생기면:
1. 빌드 로그 확인
2. 환경변수 재확인
3. 이슈 트래커에 질문하기

Good luck! 🚀

