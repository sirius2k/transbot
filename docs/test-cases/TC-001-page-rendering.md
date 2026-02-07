# TC-001: 페이지 렌더링

- **작성일**: 2026-02-07
- **작성자**: QA Team
- **마지막 업데이트**: 2026-02-07
- **상태**: ✅ 완료
- **우선순위**: P0 (Critical)
- **예상 실행 시간**: 1분 미만

## 개요

### 테스트 목적

Streamlit 앱이 정상적으로 시작되고, 타이틀/입력 영역/사이드바 등 핵심 UI 요소가 올바르게 렌더링되는지 검증합니다. 앱의 가장 기본적인 동작을 확인하는 Smoke Test입니다.

### 테스트 범위

- **UI 렌더링**: 타이틀, 입력 필드, 버튼, 사이드바 표시 확인
- **사용자 인터랙션**: 기본 UI 요소 클릭 가능 여부 확인
- **상태 관리**: Session state 초기화 확인

### 관련 FEATURE

- FEATURE-001: 영어 ↔ 한국어 양방향 번역
- FEATURE-007: 사이드바 UI (설정 섹션)

## 전제 조건

- [ ] Streamlit 앱이 실행 중이어야 함 (`streamlit run app.py`)
- [ ] 앱이 `http://localhost:8501`에서 접근 가능해야 함
- [ ] 유효한 API 키가 `.env` 파일에 설정되어 있어야 함 (OpenAI 또는 Azure)
- [ ] 브라우저가 JavaScript를 지원해야 함

## 테스트 시나리오

### 시나리오 1: 기본 페이지 로딩 및 타이틀 표시

**Given** (전제 조건)

- Streamlit 앱이 실행 중임
- 브라우저가 앱 URL에 접근 가능함

**When** (실행 동작)

- 브라우저에서 `http://localhost:8501` 접속

**Then** (예상 결과)

- 페이지가 3초 이내에 로드됨
- 타이틀이 표시됨: "🌐 TransBot" 또는 설정된 APP_TITLE
- 페이지 탭 제목이 "TransBot"으로 표시됨
- 로딩 스피너가 사라지고 메인 화면이 표시됨

---

### 시나리오 2: 입력 영역 렌더링

**Given** (전제 조건)

- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 메인 화면을 확인함

**Then** (예상 결과)

- "원문" 레이블이 표시됨
- 텍스트 입력 필드가 렌더링됨
- Placeholder 텍스트가 표시됨: "번역할 텍스트를 입력하세요... (한국어/English 자동 감지)"
- 입력 필드가 빈 상태로 초기화됨
- 통계 정보 영역이 표시됨 (초기에는 빈 상태)

---

### 시나리오 3: 사이드바 렌더링 (OpenAI Provider)

**Given** (전제 조건)

- `.env` 파일에 `AI_PROVIDER=openai` 설정됨
- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 사이드바를 확인함

**Then** (예상 결과)

- 사이드바가 화면 왼쪽에 표시됨
- "⚙️ 설정" 헤더가 표시됨
- "AI 모델 선택" 섹션이 표시됨
- 모델 선택 드롭다운이 렌더링됨 (GPT-4o, GPT-4o Mini 등)
- "번역 옵션" 섹션이 표시됨
- Help 섹션이 표시됨

---

### 시나리오 4: 사이드바 렌더링 (Azure Provider)

**Given** (전제 조건)

- `.env` 파일에 `AI_PROVIDER=azure` 설정됨
- Azure OpenAI 관련 환경 변수가 설정됨
- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 사이드바를 확인함

**Then** (예상 결과)

- 사이드바가 화면 왼쪽에 표시됨
- "⚙️ 설정" 헤더가 표시됨
- "Azure Deployment 선택" 섹션이 표시됨
- Deployment 선택 드롭다운이 렌더링됨
- "번역 옵션" 섹션이 표시됨

---

### 시나리오 5: 액션 버튼 표시

**Given** (전제 조건)

- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 입력 영역 하단을 확인함

**Then** (예상 결과)

- "🚀 번역" 버튼이 표시됨
- "🗑️ 지우기" 버튼이 표시됨
- 두 버튼이 좌우로 배치됨
- 버튼이 클릭 가능한 상태임 (disabled 아님)

## 테스트 데이터

### 입력 데이터

테스트 데이터 없음 (UI 렌더링만 확인)

### 예상 결과

| 시나리오 | 예상 결과 | 검증 방법 |
| -------- | --------- | --------- |
| 시나리오 1 | 타이틀 "🌐 TransBot" 표시 | 텍스트 존재 확인 |
| 시나리오 2 | 입력 필드 렌더링 | textarea 요소 존재 확인 |
| 시나리오 3 | 사이드바 "⚙️ 설정" 표시 | 사이드바 헤더 확인 |
| 시나리오 4 | Azure Deployment 선택 표시 | 드롭다운 존재 확인 |
| 시나리오 5 | "🚀 번역" 버튼 표시 | 버튼 요소 존재 확인 |

## UI 선택자 (Playwright 참고)

| 엘리먼트 | 선택자 | 설명 |
| -------- | ------ | ---- |
| 페이지 타이틀 | `h1:has-text("TransBot")` | 메인 타이틀 |
| 입력 필드 레이블 | `text=원문` | "원문" 레이블 |
| 입력 텍스트 영역 | `textarea[placeholder*="번역할 텍스트"]` | 메인 입력 필드 |
| 사이드바 헤더 | `text=⚙️ 설정` | 사이드바 설정 헤더 |
| 모델 선택 드롭다운 (OpenAI) | `text=AI 모델 선택` | 모델 선택 섹션 |
| Deployment 선택 (Azure) | `text=Azure Deployment 선택` | Deployment 선택 섹션 |
| 번역 버튼 | `button:has-text("🚀 번역")` | 번역 실행 버튼 |
| 지우기 버튼 | `button:has-text("🗑️ 지우기")` | 입력 초기화 버튼 |

**참고**: 향후 자동화 테스트 구현 시 앱에 `data-testid` 속성 추가를 권장합니다.

예시:

```python
st.text_area(
    "원문",
    key="input_text",
    data_testid="main-input-area"  # 추가 권장
)
```

## 실행 방법

### 수동 테스트

1. **앱 실행**

   ```bash
   streamlit run app.py
   ```

2. **브라우저 접속**
   - `http://localhost:8501` 접속

3. **시나리오 1 검증: 타이틀 확인**
   - [ ] 페이지가 3초 이내에 로드됨
   - [ ] "🌐 TransBot" 타이틀 표시
   - [ ] 브라우저 탭 제목 "TransBot" 확인

4. **시나리오 2 검증: 입력 영역 확인**
   - [ ] "원문" 레이블 표시
   - [ ] 텍스트 입력 필드 렌더링
   - [ ] Placeholder 텍스트 표시
   - [ ] 통계 영역 표시

5. **시나리오 3/4 검증: 사이드바 확인**
   - [ ] 사이드바 표시
   - [ ] "⚙️ 설정" 헤더 표시
   - [ ] 모델/Deployment 선택 드롭다운 표시
   - [ ] "번역 옵션" 섹션 표시

6. **시나리오 5 검증: 버튼 확인**
   - [ ] "🚀 번역" 버튼 표시
   - [ ] "🗑️ 지우기" 버튼 표시
   - [ ] 버튼 클릭 가능 상태 확인

### 자동 테스트 (Playwright)

```bash
# 향후 구현 예정
pytest tests/integration/test_TC_001_page_rendering.py
```

**자동화 테스트 스크립트 예시**:

```python
import pytest
from playwright.sync_api import Page, expect

def test_page_loads_with_title(page: Page):
    """시나리오 1: 기본 페이지 로딩 및 타이틀 표시"""
    page.goto("http://localhost:8501")

    # 타이틀 확인
    expect(page.locator("h1")).to_contain_text("TransBot")

def test_input_area_rendered(page: Page):
    """시나리오 2: 입력 영역 렌더링"""
    page.goto("http://localhost:8501")

    # 입력 필드 확인
    input_field = page.locator("textarea")
    expect(input_field).to_be_visible()
    expect(input_field).to_have_attribute("placeholder", "번역할 텍스트를 입력하세요...")

def test_sidebar_rendered(page: Page):
    """시나리오 3/4: 사이드바 렌더링"""
    page.goto("http://localhost:8501")

    # 사이드바 확인
    expect(page.locator("text=⚙️ 설정")).to_be_visible()
```

## 주의사항

- **로딩 시간**: 초기 로딩 시 Streamlit 초기화로 인해 2-3초 소요될 수 있음
- **캐시**: 이전 테스트의 세션 상태가 남아있을 수 있으므로, 필요시 브라우저 캐시 삭제
- **포트 충돌**: 8501 포트가 이미 사용 중이면 다른 포트로 실행됨 (8502, 8503 등)
- **API 키**: OpenAI/Azure API 키가 없으면 경고 메시지가 표시될 수 있으나, 페이지 렌더링은 정상 작동해야 함
- **Provider 설정**: 환경 변수 `AI_PROVIDER` 값에 따라 사이드바 내용이 달라짐

## 변경 이력

| 날짜 | 변경 내용 | 작성자 |
| ---- | --------- | ------ |
| 2026-02-07 | 초안 작성 | QA Team |

---

**마지막 업데이트**: 2026-02-07
