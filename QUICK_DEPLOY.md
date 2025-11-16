# 🚀 빠른 재배포 가이드

## 코드 수정 후 배포하기 (3단계)

### 1단계: 파일 추가
```bash
git add .
```
→ 모든 변경된 파일을 Git에 추가합니다.

특정 파일만 추가하려면:
```bash
git add app.py
git add templates/home.html
```

### 2단계: 커밋 (변경사항 저장)
```bash
git commit -m "수정 내용 설명"
```

예시:
```bash
git commit -m "검색 결과 개수를 5개에서 10개로 변경"
git commit -m "홈페이지 디자인 수정"
git commit -m "버그 수정: 한글 깨짐 문제 해결"
```

### 3단계: GitHub에 푸시
```bash
git push
```

→ **끝!** Render가 자동으로 재배포합니다! 🎉

---

## ⏱️ 배포 시간

```
git push 실행
    ↓
30초~1분: GitHub에 업로드
    ↓
1~3분: Render가 감지 및 빌드
    ↓
✅ 배포 완료!
```

**총 소요 시간: 2~5분**

---

## 📺 배포 상태 확인

### Render 대시보드에서 확인:
1. https://dashboard.render.com 접속
2. 프로젝트 클릭
3. **Logs** 탭에서 실시간 배포 로그 확인

배포 중:
```
=== Building...
=== Installing dependencies...
=== Deploying...
```

배포 완료:
```
✓ Build successful
✓ Deploy live
```

---

## 🔍 자주 하는 수정 예시

### 예시 1: 검색 결과 개수 변경

**수정 전 (app.py):**
```python
def search_naver_news(keyword, display=5):
```

**수정 후:**
```python
def search_naver_news(keyword, display=10):  # 5개 → 10개
```

**배포:**
```bash
git add app.py
git commit -m "검색 결과를 10개로 증가"
git push
```

### 예시 2: CSS 스타일 변경

**수정 (static/style.css):**
```css
.logo {
    font-size: 4rem;  /* 3rem → 4rem */
    color: #FF6B6B;   /* 파란색 → 빨간색 */
}
```

**배포:**
```bash
git add static/style.css
git commit -m "로고 크기 및 색상 변경"
git push
```

### 예시 3: 여러 파일 동시 수정

```bash
# 여러 파일 수정...

git add .
git commit -m "UI 전체 개선 및 버그 수정"
git push
```

---

## ⚠️ 주의사항

### 1. 환경변수 변경은 Render에서 직접!

`.env` 파일이나 API 키를 변경했다면:
- ❌ GitHub에 푸시하면 안 됨 (.gitignore에 의해 무시됨)
- ✅ Render 대시보드 → Environment → 직접 수정

### 2. 배포 실패 시

**Logs 확인:**
```
Error: Module not found
→ requirements.txt에 패키지 추가 필요

Error: Syntax error
→ 코드 문법 오류 확인
```

**해결 후 다시 푸시:**
```bash
# 오류 수정
git add .
git commit -m "배포 오류 수정"
git push
```

---

## 💡 유용한 Git 명령어

### 현재 상태 확인
```bash
git status
```
→ 어떤 파일이 수정되었는지 확인

### 변경 내용 확인
```bash
git diff
```
→ 정확히 무엇이 바뀌었는지 확인

### 커밋 히스토리 확인
```bash
git log
```
→ 이전 커밋들 확인

### 이전 버전으로 되돌리기 (조심!)
```bash
git revert HEAD
git push
```
→ 마지막 커밋 취소

---

## 🎯 실전 예제 (전체 흐름)

```bash
# 1. 코드 수정 (VS Code 등에서)
# app.py, style.css 등을 수정...

# 2. 변경사항 확인
git status

# 3. 파일 추가
git add .

# 4. 커밋
git commit -m "뉴스 카드 디자인 개선"

# 5. 푸시 (자동 배포!)
git push

# 6. Render 대시보드에서 배포 상태 확인
# 7. 2-5분 후 웹사이트에서 변경사항 확인! ✅
```

---

## 🚀 요약

| 단계 | 명령어 | 설명 |
|------|--------|------|
| 1 | 파일 수정 | VS Code 등에서 코드 수정 |
| 2 | `git add .` | 변경사항 추가 |
| 3 | `git commit -m "설명"` | 변경사항 저장 |
| 4 | `git push` | GitHub에 업로드 |
| 5 | 자동! | Render가 자동 배포 ✨ |

---

## 🎉 핵심 포인트

✅ **자동 배포** - Render가 GitHub를 감시하고 자동으로 배포
✅ **빠른 배포** - 2~5분이면 완료
✅ **무료** - 무제한 재배포 가능
✅ **간단** - git push만 하면 끝!

---

**더 궁금한 점이 있으면 언제든 물어보세요!** 🚀

