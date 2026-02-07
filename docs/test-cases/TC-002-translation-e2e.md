# TC-002: 번역 E2E 플로우

- **작성일**: 2026-02-08
- **작성자**: QA Team
- **마지막 업데이트**: 2026-02-08
- **상태**: ✅ 완료
- **우선순위**: P0 (Critical)
- **예상 실행 시간**: 1분 미만

## 개요

### 테스트 목적

사용자가 텍스트를 입력하고 번역 버튼을 클릭하여 번역 결과를 받는 전체 E2E 플로우를 검증합니다. TransBot의 핵심 기능인 양방향 번역(영어↔한국어), Markdown 포맷 보존, 다중 스타일 번역이 정상적으로 동작하는지 확인합니다.

### 테스트 범위

- **사용자 인터랙션**: 텍스트 입력, 번역 버튼 클릭, 복사 버튼 동작
- **데이터 처리**: AI API 호출, 번역 결과 생성, 언어 자동 감지
- **상태 관리**: Session state 업데이트, 번역 히스토리 관리

### 관련 FEATURE

- FEATURE-001: 영어 ↔ 한국어 양방향 번역
- FEATURE-002: Markdown 포맷 보존
- FEATURE-004: 다중 스타일 번역 (캐주얼/포멀)

## 전제 조건

- [ ] Streamlit 앱이 실행 중이어야 함 (`http://localhost:8501`)
- [ ] 유효한 API 키가 설정되어 있어야 함 (OpenAI 또는 Azure)
- [ ] 인터넷 연결이 정상적으로 동작해야 함 (API 호출 가능)
- [ ] 브라우저가 JavaScript를 지원해야 함

## 테스트 시나리오

### 시나리오 1: 영어 → 한국어 번역 (Happy Path)

**Given** (전제 조건)

- Streamlit 앱이 실행 중
- 페이지가 정상적으로 로드됨
- 입력 필드가 빈 상태

**When** (실행 동작)

- 사용자가 영어 텍스트를 입력: "Hello, how are you today?"
- "🚀 번역" 버튼을 클릭

**Then** (예상 결과)

- 번역이 진행 중임을 나타내는 상태 표시
- 번역 결과가 "번역 결과" 섹션에 표시됨
- 번역 결과에 "안녕하세요" 또는 유사한 인사말이 포함됨
- 언어 감지 결과: "English"
- 통계 정보가 표시됨 (글자 수, 단어 수, 문장 수)
- "📋 복사" 버튼이 활성화됨

---

### 시나리오 2: 한국어 → 영어 번역 (Happy Path)

**Given** (전제 조건)

- Streamlit 앱이 실행 중
- 페이지가 정상적으로 로드됨
- 입력 필드가 빈 상태

**When** (실행 동작)

- 사용자가 한국어 텍스트를 입력: "안녕하세요, 오늘 날씨가 좋네요."
- "🚀 번역" 버튼을 클릭

**Then** (예상 결과)

- 번역 결과가 "번역 결과" 섹션에 표시됨
- 번역 결과에 "Hello" 또는 "Hi" 등의 인사말이 포함됨
- 언어 감지 결과: "Korean"
- 통계 정보가 표시됨 (글자 수, 단어 수, 문장 수)
- "📋 복사" 버튼이 활성화됨

---

### 시나리오 3: Markdown 포맷 보존 번역

**Given** (전제 조건)

- Streamlit 앱이 실행 중
- 페이지가 정상적으로 로드됨
- "원문 유지" 옵션이 체크됨

**When** (실행 동작)

- 사용자가 Markdown 포맷 텍스트를 입력:
  ```
  # Hello World

  This is a **bold** text and this is *italic*.

  - Item 1
  - Item 2
  ```
- "🚀 번역" 버튼을 클릭

**Then** (예상 결과)

- 번역 결과에 Markdown 포맷이 보존됨
- `#`, `**`, `*`, `-` 등의 Markdown 문법이 유지됨
- 번역된 텍스트와 원문이 함께 표시됨
- 번역 결과가 Markdown으로 올바르게 렌더링됨

---

### 시나리오 4: 다중 스타일 번역 (캐주얼 vs 포멀)

**Given** (전제 조건)

- Streamlit 앱이 실행 중
- 페이지가 정상적으로 로드됨
- "다중 스타일" 옵션이 체크됨
- "캐주얼" 스타일이 선택됨

**When** (실행 동작)

- 사용자가 영어 텍스트를 입력: "Please submit the report by tomorrow."
- "🚀 번역" 버튼을 클릭

**Then** (예상 결과)

- "캐주얼" 스타일 번역 결과가 표시됨 (예: "내일까지 보고서 제출해줘")
- "포멀" 스타일 번역 결과가 표시됨 (예: "내일까지 보고서를 제출해 주시기 바랍니다")
- 두 스타일이 명확히 구분되어 표시됨
- 각 스타일별로 복사 버튼이 활성화됨

## 테스트 데이터

### 입력 데이터

| 항목 | 값 | 설명 |
| ---- | -- | ---- |
| 영어 텍스트 (짧음) | "Hello, how are you today?" | 기본 인사말 |
| 한국어 텍스트 (짧음) | "안녕하세요, 오늘 날씨가 좋네요." | 기본 인사말 |
| Markdown 텍스트 | "# Hello\n\n**bold** and *italic*" | 포맷 보존 테스트 |
| 포멀 영어 텍스트 | "Please submit the report by tomorrow." | 다중 스타일 테스트 |

### 예상 결과

| 시나리오 | 예상 결과 | 검증 방법 |
| -------- | --------- | --------- |
| 영어→한국어 | "안녕하세요" 또는 유사 인사말 포함 | 텍스트 포함 확인 |
| 한국어→영어 | "Hello" 또는 "Hi" 포함 | 텍스트 포함 확인 |
| Markdown 보존 | `#`, `**`, `*` 문법 유지 | 정규식 매칭 |
| 다중 스타일 | 캐주얼/포멀 두 스타일 모두 표시 | 섹션 구분 확인 |

## UI 선택자 (Playwright 참고)

| 엘리먼트 | 선택자 | 설명 |
| -------- | ------ | ---- |
| 입력 필드 | `textarea[placeholder*="번역할 텍스트"]` | 메인 입력 영역 |
| 번역 버튼 | `button:has-text("🚀 번역")` | 번역 실행 버튼 |
| 번역 결과 영역 | `text=번역 결과` | 번역 결과 헤더 |
| 복사 버튼 | `button:has-text("📋 복사")` | 결과 복사 버튼 |
| 언어 감지 결과 | `text=감지된 언어` | 언어 감지 정보 |
| 통계 정보 | `text=글자 수` | 텍스트 통계 |
| 원문 유지 체크박스 | `label:has-text("원문 유지")` | Markdown 옵션 |
| 다중 스타일 체크박스 | `label:has-text("다중 스타일")` | 다중 스타일 옵션 |

**참고**: 향후 자동화 테스트 구현 시 앱에 `data-testid` 속성 추가를 권장합니다.

## 실행 방법

### 수동 테스트

1. **앱 실행**

   ```bash
   streamlit run app.py
   ```

2. **시나리오 1 검증: 영어 → 한국어**
   - [ ] "Hello, how are you today?" 입력
   - [ ] "🚀 번역" 버튼 클릭
   - [ ] 번역 결과에 "안녕하세요" 포함 확인
   - [ ] 언어 감지 "English" 확인
   - [ ] 통계 정보 표시 확인

3. **시나리오 2 검증: 한국어 → 영어**
   - [ ] "안녕하세요, 오늘 날씨가 좋네요." 입력
   - [ ] "🚀 번역" 버튼 클릭
   - [ ] 번역 결과에 "Hello" 또는 "Hi" 포함 확인
   - [ ] 언어 감지 "Korean" 확인

4. **시나리오 3 검증: Markdown 보존**
   - [ ] 사이드바에서 "원문 유지" 체크
   - [ ] Markdown 텍스트 입력
   - [ ] 번역 후 Markdown 문법 유지 확인

5. **시나리오 4 검증: 다중 스타일**
   - [ ] 사이드바에서 "다중 스타일" 체크
   - [ ] 포멀 영어 텍스트 입력
   - [ ] 캐주얼/포멀 두 스타일 모두 표시 확인

### 자동 테스트 (pytest-bdd + Playwright)

#### 설치 방법

```bash
# 이미 설치되어 있음 (TC-001 설정 시 완료)
pip install pytest-bdd playwright pytest-playwright
playwright install chromium
```

#### 실행 방법

```bash
# Streamlit 앱 실행 (별도 터미널)
streamlit run app.py

# 전체 feature 실행
pytest tests/integration/features/TC-002-translation-e2e.feature --browser chromium --no-cov -v

# 특정 시나리오만 실행
pytest tests/integration/features/TC-002-translation-e2e.feature -k "영어 한국어" --browser chromium --no-cov -v

# 상세 출력
pytest tests/integration/features/TC-002-translation-e2e.feature --browser chromium --no-cov -vv

# HTML 리포트 생성
pytest tests/integration/features/TC-002-translation-e2e.feature --browser chromium --no-cov --html=report.html
```

## 주의사항

- **API 키**: 유효한 API 키가 없으면 번역이 실패합니다
- **API 타임아웃**: 네트워크 지연 시 타임아웃 설정 조정 필요 (기본 60초)
- **번역 품질**: AI 모델의 번역 결과는 매번 다를 수 있으므로, 정확한 텍스트 매칭보다는 키워드 포함 여부로 검증
- **Markdown 렌더링**: Streamlit의 `st.markdown()` 동작에 따라 렌더링 결과가 다를 수 있음
- **다중 스타일**: "다중 스타일" 옵션은 "원문 유지" 옵션과 함께 사용할 수 없음
- **레이트 리밋**: OpenAI API는 분당 요청 수 제한이 있으므로, 빠른 반복 테스트 시 주의

## 변경 이력

| 날짜 | 변경 내용 | 작성자 |
| ---- | --------- | ------ |
| 2026-02-08 | 초안 작성 | QA Team |

---

**마지막 업데이트**: 2026-02-08
