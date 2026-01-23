# PRD: TransBot - 영어-한국어 번역 애플리케이션

## 1. 제품 개요

### 1.1 제품명

**TransBot** - AI 기반 영어-한국어 양방향 번역기

### 1.2 목적

OpenAI의 GPT 모델을 활용하여 사용자에게 빠르고 정확한 영어-한국어 양방향 번역 서비스를 제공하는 웹 기반 애플리케이션

### 1.3 타겟 사용자

- 영어-한국어 번역이 필요한 일반 사용자
- 간단한 문서나 텍스트를 번역해야 하는 직장인
- 외국어 학습자
- 개발자 및 번역 도구가 필요한 전문가

## 2. 핵심 기능

### 2.1 양방향 번역 (MVP)

- **영어 → 한국어** 번역
- **한국어 → 영어** 번역
- 라디오 버튼을 통한 번역 방향 선택

### 2.2 사용자 인터페이스

- 간결하고 직관적인 Streamlit 기반 웹 UI
- **좌측 사이드바**:
  - OpenAI API 키 입력 (선택)
  - AI 모델 선택 드롭다운 (5개 모델)
- **메인 영역**:
  - 자동 번역 안내 메시지
  - Markdown 지원 안내 메시지
  - 입력 텍스트 영역 (200px 높이)
    - 좌측: "원문 (Markdown 지원)" 라벨
    - 우측: 실시간 번역 방향 표시 (🇰🇷 → 🇺🇸 또는 🇺🇸 → 🇰🇷)
    - 우측: 글자수 / 토큰수 실시간 표시
  - 번역 버튼 (전체 너비)
  - 번역 결과 탭 뷰:
    - 📄 렌더링: Markdown이 적용된 결과
    - 📝 Markdown 원본: 복사 가능한 원본 코드
- 실시간 번역 진행 상태 표시 (스피너)

### 2.3 API 키 관리

- 환경 변수를 통한 API 키 설정 (.env 파일)
- 사이드바를 통한 수동 API 키 입력 (대체 옵션)
- API 키 미입력 시 경고 메시지 표시

### 2.4 AI 번역 엔진

- 다양한 OpenAI GPT 모델 지원 (GPT-4o, GPT-4o Mini, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- GPT-4o Mini를 기본 모델로 설정 (가성비 우수)
- Temperature 0.3으로 일관된 번역 품질 유지
- 전문 번역가 페르소나 시스템 프롬프트
- **Markdown 포맷 보존**: 볼드, 이탤릭, 헤딩, 리스트, 링크, 코드 블록, 인용문, 표 등 모든 포맷 유지
- **자동 언어 감지**: 입력된 텍스트의 언어를 자동으로 판별하여 번역 방향 설정
  - 한글 문자와 영문 알파벳 비율 분석
  - 한글 50% 이상 → 한국어로 감지 → 영어로 번역
  - 영문 50% 이상 → 영어로 감지 → 한국어로 번역

## 3. 기술 스택

### 3.1 프론트엔드

- **Streamlit** 1.28.0 이상: 웹 인터페이스 프레임워크

### 3.2 백엔드/API

- **OpenAI API** 1.0.0 이상: 다양한 GPT 모델 활용
- **Python 3.x**: 메인 개발 언어
- **tiktoken** 0.5.0 이상: 토큰 수 계산 라이브러리

### 3.3 환경 관리

- **python-dotenv** 1.0.0 이상: 환경 변수 관리

## 4. 사용자 플로우

```text
1. 사용자가 애플리케이션 접속
   ↓
2. (선택) API 키 미설정 시 사이드바에서 입력
   ↓
3. 번역 방향 선택 (영어→한국어 또는 한국어→영어)
   ↓
4. 원문 텍스트 입력
   ↓
5. "번역하기" 버튼 클릭
   ↓
6. 번역 진행 중 스피너 표시
   ↓
7. 번역 결과 표시
   ↓
8. (선택) 새로운 텍스트 번역 반복
```

## 5. 기능 요구사항

### 5.1 필수 요구사항 (Must Have)

- [x] 영어 → 한국어 번역
- [x] 한국어 → 영어 번역
- [x] OpenAI API 연동
- [x] 기본 웹 UI
- [x] 에러 처리 (API 오류, 빈 입력 등)
- [x] AI 모델 선택 기능 (5개 모델 지원)
- [x] 자동 언어 감지 (한국어/영어)
- [x] 글자수/토큰수 실시간 표시
- [x] Markdown 포맷 지원 및 보존
- [x] 번역 결과 탭 뷰 (렌더링/Markdown 원본)

### 5.2 향후 고려사항 (Nice to Have)

#### 단기 (Phase 2)

- [x] Markdown 포맷 지원 (볼드, 이탤릭, 리스트, 링크 등)
- [x] 번역 결과 탭 뷰 (렌더링/Markdown 원본)
- [x] 포맷 유지 번역 (Markdown 포맷 보존)
- [x] 자동 언어 감지 (한국어/영어 자동 판별)
- [x] 글자수/토큰수 실시간 표시 (tiktoken 사용)
- [ ] 번역 히스토리 저장
- [ ] 즐겨찾기 기능
- [ ] 번역 결과 원클릭 복사 버튼 (현재 Markdown 원본 탭에 내장된 복사 기능 제공)

#### 중기 (Phase 2.5)

- [ ] 파일 업로드를 통한 일괄 번역
- [ ] 번역 품질 피드백 기능
- [ ] 번역 스타일 선택 (격식체/비격식체)
- [ ] 번역 히스토리 클라우드 동기화

#### 장기 (Phase 3)

- [ ] Rich Text Editor 통합 (WYSIWYG 편집)
- [ ] 다국어 지원 확장 (중국어, 일본어 등)
- [ ] 용어집(Glossary) 기능
- [ ] 사용량 통계 및 비용 추적
- [ ] 다양한 AI 모델 확장 (Claude, Gemini 등)

### 5.3 구현 완료된 주요 기능 (Phase 1.5)

#### 5.3.1 자동 언어 감지

**구현 상태**: ✅ 완료

**구현 내용**:

- 입력 텍스트의 언어를 자동으로 감지하여 번역 방향 자동 설정
- 한글 문자(가-힣)와 영문 알파벳 비율 분석
- 한글이 50% 이상이면 한국어로 판별 → 영어로 번역
- 영문이 50% 이상이면 영어로 판별 → 한국어로 번역
- 실시간 번역 방향 표시: 🇰🇷 → 🇺🇸 또는 🇺🇸 → 🇰🇷

**사용자 경험**:

- 번역 방향 선택 버튼 제거로 UI 단순화
- 텍스트 입력 시 자동으로 번역 방향 표시
- 언어 감지 실패 시 명확한 에러 메시지 제공

**기술 구현**:

```python
def detect_language(text: str) -> str:
    korean_chars = sum(1 for char in text if '\uac00' <= char <= '\ud7a3')
    english_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)
    total_alpha = korean_chars + english_chars

    if total_alpha == 0:
        return "unknown"

    if korean_chars / total_alpha > 0.5:
        return "Korean"
    else:
        return "English"
```

#### 5.3.2 글자수 / 토큰수 실시간 표시

**구현 상태**: ✅ 완료

**구현 내용**:

- tiktoken 라이브러리를 사용한 정확한 토큰 수 계산
- 선택된 AI 모델에 맞는 인코딩 방식 적용
- 입력 텍스트 우측 상단에 실시간 표시
- 천 단위 쉼표 포맷팅 (예: 1,234자 / 567 토큰)

**표시 정보**:

- 번역 방향 (🇰🇷 → 🇺🇸 또는 🇺🇸 → 🇰🇷)
- 글자수 (입력 텍스트의 전체 문자 수)
- 토큰수 (선택된 AI 모델 기준)

**비용 관리**:

- 사용자가 번역 전 예상 토큰 수를 확인하여 비용 예측 가능
- 토큰 수 기반으로 API 호출 비용 사전 인지

#### 5.3.3 Markdown 포맷 지원 및 보존

**구현 상태**: ✅ 완료

**구현 내용**:

- 입력 시 Markdown 문법 안내 메시지 표시
- 시스템 프롬프트에 Markdown 포맷 보존 지시 추가
- 번역 결과를 탭 뷰로 제공:
  - 📄 렌더링: Markdown이 적용된 시각적 결과
  - 📝 Markdown 원본: 복사 가능한 원본 코드

**지원하는 Markdown 문법**:

- 볼드: `**텍스트**`
- 이탤릭: `*텍스트*`
- 코드: `` `코드` ``
- 링크: `[텍스트](URL)`
- 리스트: `- 항목` 또는 `1. 항목`
- 인용문: `> 인용문`
- 헤딩: `#`, `##`, `###`
- 코드 블록: ` ``` `
- 표 (테이블)

**시스템 프롬프트**:

```text
You are a professional translator. Translate the following {source} text to {target}.
IMPORTANT: Preserve all Markdown formatting (bold, italic, headings, lists, links,
code blocks, blockquotes, tables, etc.) in the translation. Only respond with the
translation, nothing else.
```

#### 5.3.4 사이드바 UI 개선

**구현 상태**: ✅ 완료

**구현 내용**:

- 좌측 사이드바에 설정 섹션 구성
- OpenAI API 키 입력 (비밀번호 타입)
- AI 모델 선택 드롭다운 (5개 모델)
- 메인 영역은 번역 작업에 집중

**사이드바 구성**:

```text
⚙️ 설정
├── OpenAI API Key (선택)
└── AI 모델 선택:
    ├── GPT-4o Mini (추천 - 가성비) [기본값]
    ├── GPT-4o (최고 품질)
    ├── GPT-4 Turbo
    ├── GPT-4
    └── GPT-3.5 Turbo (빠름)
```

### 5.4 포맷 텍스트 지원 상세 계획

#### 배경

사용자들이 문서 번역 시 텍스트 포맷(볼드, 이탤릭, 리스트 등)을 유지하면서 번역하고자 하는 니즈가 있음. 현재는 일반 텍스트만 지원하여 포맷 정보가 손실됨.

#### 기술적 가능성

**✅ 가능**: Streamlit의 `st.markdown()` 네이티브 지원, OpenAI API의 Markdown 포맷 이해 능력

**제약사항**: Streamlit의 `st.text_area()`는 WYSIWYG 편집 미지원

#### Phase 2: Markdown 기반 접근 (권장)

**구현 방법**:

- 입력: `st.text_area()`로 Markdown 문법 입력 받기
- 처리: GPT 모델에 Markdown 포맷 보존 지시 (시스템 프롬프트 수정)
- 출력: `st.tabs()`로 렌더링 뷰와 Markdown 원본 뷰 제공

**지원 포맷**:

- 볼드 (`**text**`), 이탤릭 (`*text*`)
- 헤딩 (`#`, `##`, `###`)
- 리스트 (`-`, `1.`)
- 링크 (`[text](url)`)
- 코드 블록 (` ``` `)
- 인용문 (`>`)
- 표 (테이블)

**장점**:

- 추가 라이브러리 불필요
- 구현 난이도 낮음 (⭐⭐☆☆☆)
- GPT 모델과 자연스럽게 호환
- 예상 개발 시간: 30분 - 1시간

**단점**:

- 사용자가 Markdown 문법 학습 필요
- WYSIWYG 편집 불가

#### Phase 3: Rich Text Editor (선택)

**구현 방법**:

- `streamlit-quill` 또는 커스텀 컴포넌트 사용
- HTML/Markdown 변환 레이어 필요

**장점**:

- WYSIWYG 편집 가능
- 사용자 친화적

**단점**:

- 추가 라이브러리 필요
- 구현 복잡도 증가 (⭐⭐⭐☆☆)
- HTML 보안 이슈 고려 필요

#### 시스템 프롬프트 예시

```text
You are a professional translator.
Translate the following {source} text to {target}.
IMPORTANT: Preserve all Markdown formatting (bold, italic, lists, links, etc.) in the translation.
Only respond with the translation, nothing else.
```

#### UI 예시

```python
# 입력
st.info("💡 **볼드**, *이탤릭*, - 리스트 등 Markdown 문법 사용 가능")
input_text = st.text_area("원문 (Markdown 지원)", height=200)

# 출력
tab1, tab2 = st.tabs(["렌더링", "Markdown 원본"])
with tab1:
    st.markdown(result)
with tab2:
    st.code(result, language="markdown")
```

#### 성공 기준

- Markdown 포맷이 80% 이상 정확히 보존됨
- 사용자가 렌더링 결과를 시각적으로 확인 가능
- 복잡한 포맷(표, 중첩 리스트)도 처리 가능

## 6. 비기능 요구사항

### 6.1 성능

- 번역 응답 시간: 평균 5초 이내
- 최대 입력 텍스트 길이: 제한 없음 (OpenAI API 토큰 한도 내)

### 6.2 보안

- API 키는 환경 변수 또는 암호화된 입력으로 관리
- API 키는 코드에 하드코딩하지 않음
- .gitignore를 통한 민감 정보 제외

### 6.3 사용성

- 직관적이고 간결한 UI
- 명확한 에러 메시지 제공
- 반응형 디자인 (중앙 정렬 레이아웃)

### 6.4 확장성

- 모듈화된 코드 구조로 향후 기능 추가 용이
- 다른 AI 모델 추가 가능한 구조

## 7. 제약사항 및 리스크

### 7.1 제약사항

- OpenAI API 키 필수 (유료 서비스)
- 인터넷 연결 필수
- OpenAI API 사용량 제한에 따른 비용 발생

### 7.2 리스크

- API 요청 실패 가능성
- API 비용 증가 리스크
- OpenAI 서비스 중단 시 서비스 불가
- 번역 품질이 모델 성능에 의존

### 7.3 대응 방안

- 에러 핸들링 및 사용자 친화적 에러 메시지 제공
- API 사용량 모니터링 기능 추가 고려
- 대체 AI 모델 옵션 제공 고려

## 8. 성공 지표 (KPI)

- 번역 완료율: 95% 이상
- 평균 응답 시간: 5초 이내
- 에러 발생률: 5% 이하
- 사용자 재방문율

## 9. 릴리스 계획

### Phase 1 (Complete - MVP)

**릴리스 날짜**: 2026-01-24 이전

- [x] 기본 양방향 번역 기능 (영어↔한국어)
- [x] Streamlit 기반 웹 UI
- [x] OpenAI API 연동
- [x] 다양한 AI 모델 선택 (5개 모델 지원)
- [x] 에러 처리 및 사용자 피드백
- [x] 가상환경 설정 가이드

### Phase 1.5 (Complete - Enhanced MVP)

**릴리스 날짜**: 2026-01-24

- [x] 자동 언어 감지 (한국어/영어 자동 판별)
- [x] 글자수/토큰수 실시간 표시 (tiktoken 통합)
- [x] Markdown 문법 지원 (볼드, 이탤릭, 리스트, 링크, 코드 블록, 표 등)
- [x] Markdown 포맷 보존 번역 (시스템 프롬프트 개선)
- [x] 번역 결과 탭 뷰 (📄 렌더링 / 📝 Markdown 원본)
- [x] Markdown 사용 가이드 UI 추가
- [x] 사이드바 UI 개선 (설정 섹션)
- [x] 번역 방향 실시간 표시 (🇰🇷 ↔ 🇺🇸)

**주요 개선사항**:

1. **UX 단순화**: 번역 방향 선택 버튼 제거, 자동 감지로 대체
2. **비용 투명성**: 토큰 수 실시간 표시로 API 비용 예측 가능
3. **문서 번역**: Markdown 포맷 완벽 지원으로 기술 문서 번역 가능
4. **전문성 향상**: 렌더링 뷰와 원본 뷰 제공으로 번역 품질 검증 용이

### Phase 2 (단기 - 3개월)

#### 2.1 사용성 개선 (우선순위: 높음)

- [ ] 번역 히스토리 저장 (로컬 스토리지)
- [ ] 즐겨찾기 기능
- [ ] 번역 결과 원클릭 복사 버튼 (메인 화면에 추가)
- [ ] 번역 스타일 선택 (격식체/비격식체)

#### 2.2 고급 기능 (우선순위: 중간)

- [ ] 번역 품질 피드백 (👍/👎)
- [ ] 사용자 설정 저장
- [ ] 키보드 단축키 지원 (Ctrl+Enter로 번역 등)

### Phase 2.5 (중기 - 6개월)

- [ ] 파일 업로드 일괄 번역 (.txt, .md)
- [ ] Rich Text Editor 통합 (WYSIWYG)
- [ ] 사용자 인증 및 개인화
- [ ] 번역 히스토리 클라우드 동기화

### Phase 3 (장기 - 12개월)

- [ ] 모바일 앱 개발 (React Native)
- [ ] 다국어 지원 확장 (중국어, 일본어, 스페인어 등)
- [ ] 엔터프라이즈 기능 (팀 협업, 용어집 관리)
- [ ] REST API 서비스 제공
- [ ] AI 모델 확장 (Claude, Gemini 등)
- [ ] 사용량 통계 및 비용 추적 대시보드

## 10. 부록

### 10.1 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# 애플리케이션 실행
streamlit run app.py
```

### 10.2 프로젝트 구조

```text
transbot/
├── app.py                    # 메인 애플리케이션 파일
├── requirements.txt          # Python 의존성
├── .env.example             # 환경 변수 템플릿
├── .gitignore               # Git 제외 파일 목록
└── PRD.md                   # 제품 요구사항 문서 (본 문서)
```

### 10.3 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [OpenAI API 문서](https://platform.openai.com/docs/)
- [GPT-4o-mini 모델 정보](https://platform.openai.com/docs/models/)
