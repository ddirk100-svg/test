# 🎯 AI 퍼블리싱 총괄 가이드

> “구조적으로 설계하고, 시각적으로 정돈하며, 동적으로 반응하라.”
> 

---

## 🧩 1️⃣ HTML — 구조의 언어

### 🎯 목적

> 의미 있고 시멘틱한 구조를 만든다.
> 
> 
> “보이는 모양”이 아니라, “의도를 설명하는 마크업”이 되도록.
> 

### 🧱 핵심 원칙

| 항목 | 설명 | 예시 |
| --- | --- | --- |
| **시멘틱 태그 사용** | 역할이 명확한 태그로 구조화 | `<header>`, `<nav>`, `<main>`, `<footer>` |
| **계층적 구조 유지** | 큰 틀 → 세부 구성 순서대로 마크업 | `<section>` 안에 `<article>` |
| **클래스명 규칙화** | 기능 기반 이름 | `btn-login`, `card-item` |
| **불필요한 div 최소화** | 의미 없는 div 남용 금지 | 콘텐츠 역할이 있을 때만 사용 |

### 💬 작성 예시

```html
<header>
  <nav class="gnb">
    <a href="#" class="logo">Brand</a>
    <ul class="menu">
      <li><a href="#">서비스</a></li>
      <li><a href="#">가격</a></li>
    </ul>
    <button class="btn-login">로그인</button>
  </nav>
</header>

```

### ✅ 체크리스트

- [ ]  header / main / footer 구조가 명확한가?
- [ ]  class명이 역할을 설명하는가?
- [ ]  불필요한 태그가 없는가?

---

## 🎨 2️⃣ CSS — 시각의 언어

### 🎯 목적

> 화면의 구조를 정돈하고, 디자인을 코드로 정확히 전달한다.
> 
> 
> **flex / grid / 여백 / 색상 / 반응형**의 균형을 맞춘다.
> 

### 🧭 핵심 3단 구조

| 단계 | 의미 | 대표 속성 | 예시 |
| --- | --- | --- | --- |
| **Display (공간 설정)** | 요소의 무대 정의 | `display` | `block`, `inline`, `flex`, `grid` |
| **Layout (정렬 규칙)** | 자식 요소의 배치 규칙 | `justify-content`, `align-items`, `gap` | `center`, `space-between` |
| **Style (시각 꾸밈)** | 각 요소의 시각 표현 | `margin`, `padding`, `font-size`, `color` | `color:#fff; padding:12px;` |

### 💬 작성 예시

```css
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  background: #f8f9fa;
}

.btn-login {
  padding: 10px 20px;
  color: #fff;
  background: #2f6feb;
  border-radius: 6px;
}

```

### ✅ 체크리스트

- [ ]  display / layout / style 구조가 명확히 구분되어 있는가?
- [ ]  position 남용 없이 flex/grid로 정렬했는가?
- [ ]  반응형 전환(`@media`)이 자연스러운가?

---

## ⚡️ 3️⃣ JavaScript — 동작의 언어

### 🎯 목적

> 사용자의 행동(Event)에 따라 웹페이지가 반응하게 만든다.
> 
> 
> 즉, **“무엇을 → 언제 → 어떻게”**의 흐름으로 코드를 짠다.
> 

### 🔄 핵심 3단 구조

| 단계 | 설명 | 예시 |
| --- | --- | --- |
| **선택 (Select)** | 어떤 요소를 조작할지 정함 | `document.getElementById("btn")` |
| **반응 (Event)** | 언제 동작할지를 지정 | `button.addEventListener("click", …)` |
| **행동 (Action)** | 어떤 결과를 낼지 정의 | `alert()`, `style 변경`, `데이터 갱신` |

### 💬 작성 예시

```html
<button id="helloBtn">눌러봐!</button>

<script>
  const button = document.getElementById("helloBtn");
  button.addEventListener("click", () => {
    alert("안녕! 👋");
  });
</script>

```

### ✅ 체크리스트

- [ ]  addEventListener 기반으로 이벤트 연결했는가?
- [ ]  inline JS(`onclick=""`) 없이 구조적으로 분리했는가?
- [ ]  함수 단위로 역할이 나누어졌는가?
- [ ]  변수명, 함수명이 명확한 의미를 가지는가?

---

## 🤖 AI 출력 시 공통 규칙 (HTML + CSS + JS)

| 항목 | 원칙 | 이유 |
| --- | --- | --- |
| **구조 분리** | HTML, CSS, JS는 반드시 분리 | 유지보수와 재사용성 향상 |
| **시멘틱 우선** | 의미 기반 태그 우선 사용 | SEO, 접근성 강화 |
| **position 최소화** | `absolute` 대신 `flex/grid` | 반응형 구조 안정 |
| **이벤트 구조화** | `addEventListener`로 연결 | 역할 분리 및 코드 가독성 향상 |
| **일관된 네이밍** | kebab-case 또는 camelCase 통일 | 협업 및 가독성 향상 |
| **중복 제거** | 공통 속성은 상위 요소로 이동 | 코드 간결화 |

---

## 💬 AI 프롬프트 예시

```
다음 디자인을 기반으로 구조적이고 반응형인 웹 페이지를 만들어줘.
1. HTML은 시멘틱하게 작성하고, header/main/footer 구조를 포함해줘.
2. CSS는 display, layout, style 단계로 작성하고 flex/grid를 활용해줘.
3. JavaScript는 addEventListener 기반으로 이벤트를 연결하고,
   “무엇을 → 언제 → 어떻게” 흐름으로 구성해줘.
4. inline 스타일이나 inline JS는 사용하지 마.

```

---

## ✅ 최종 점검표

| 영역 | 질문 | 예시 기준 |
| --- | --- | --- |
| **HTML** | 구조가 시멘틱하고 논리적인가? | `<header>`, `<main>`, `<footer>` |
| **CSS** | display–layout–style이 명확히 분리되었는가? | `flex`, `gap`, `margin`, `color` |
| **JS** | 선택–반응–행동 구조가 있는가? | `addEventListener("click", …)` |
| **통합성** | 세 언어가 역할을 분리하면서 유기적으로 작동하는가? | 구조 + 시각 + 동작이 일관됨 |

---

## 🧠 한 문장 요약

> HTML은 구조를 세우고, CSS는 형태를 만들고, JS는 반응을 준다.
> 
> 
> 좋은 퍼블리싱이란 “보여지는 것”보다 “읽히는 구조”를 만드는 일이다.
>