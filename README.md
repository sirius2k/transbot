# TransBot 🌐

AI 기반 영어-한국어 양방향 번역 웹 애플리케이션

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)

## 📋 목차

- [소개](#소개)
- [주요 기능](#주요-기능)
- [시작하기](#시작하기)
  - [필수 요구사항](#필수-요구사항)
  - [설치 방법](#설치-방법)
  - [환경 설정](#환경-설정)
- [사용법](#사용법)
- [프로젝트 구조](#프로젝트-구조)
- [기술 스택](#기술-스택)
- [문제 해결](#문제-해결)
- [향후 계획](#향후-계획)
- [라이선스](#라이선스)

## 소개

TransBot은 OpenAI의 GPT-4o-mini 모델을 활용하여 빠르고 정확한 영어-한국어 번역 서비스를 제공하는 웹 애플리케이션입니다. Streamlit 기반의 직관적인 인터페이스로 누구나 쉽게 사용할 수 있습니다.

### 왜 TransBot인가?

- 🚀 **빠른 번역**: GPT-4o-mini 모델을 사용한 고품질 번역
- 🔄 **양방향 지원**: 영어→한국어, 한국어→영어 모두 지원
- 💡 **간편한 사용**: 복잡한 설정 없이 바로 사용 가능
- 🎨 **직관적인 UI**: Streamlit 기반의 깔끔한 인터페이스

## 주요 기능

- ✅ 영어 → 한국어 번역
- ✅ 한국어 → 영어 번역
- ✅ 실시간 번역 진행 상태 표시
- ✅ API 키 안전 관리 (환경 변수 또는 사이드바 입력)
- ✅ 에러 처리 및 사용자 친화적 메시지

## 시작하기

### 필수 요구사항

- Python 3.x
- OpenAI API 키 ([발급 받기](https://platform.openai.com/api-keys))
- 인터넷 연결

### 설치 방법

1. **저장소 클론**

   ```bash
   git clone https://github.com/yourusername/transbot.git
   cd transbot
   ```

2. **의존성 설치**

   ```bash
   pip install -r requirements.txt
   ```

### 환경 설정

1. **환경 변수 파일 생성**

   ```bash
   cp .env.example .env
   ```

2. **.env 파일에 API 키 입력**

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   > 💡 **팁**: API 키는 [OpenAI 플랫폼](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

## 사용법

### 1. 애플리케이션 실행

```bash
streamlit run app.py
```

실행하면 브라우저가 자동으로 열리며 `http://localhost:8501`에서 애플리케이션에 접근할 수 있습니다.

### 2. API 키 설정 (선택)

환경 변수로 API 키를 설정하지 않은 경우, 사이드바에서 직접 입력할 수 있습니다.

### 3. 번역하기

1. 번역 방향을 선택합니다 (영어 → 한국어 또는 한국어 → 영어)
2. 원문 텍스트를 입력합니다
3. "번역하기" 버튼을 클릭합니다
4. 번역 결과를 확인합니다

### 사용 예시

**영어 → 한국어 번역**

```text
입력: Hello, how are you today?
출력: 안녕하세요, 오늘 어떻게 지내세요?
```

**한국어 → 영어 번역**

```text
입력: 오늘 날씨가 정말 좋네요.
출력: The weather is really nice today.
```

## 프로젝트 구조

```text
transbot/
├── app.py                    # 메인 애플리케이션 파일
├── requirements.txt          # Python 의존성 목록
├── .env.example             # 환경 변수 템플릿
├── .gitignore               # Git 제외 파일 목록
├── PRD.md                   # 제품 요구사항 문서
├── CLAUDE.md                # Claude AI 작업 가이드
└── README.md                # 프로젝트 소개 문서 (본 문서)
```

## 기술 스택

### 프론트엔드

- **Streamlit** 1.28.0+: 웹 인터페이스 프레임워크

### 백엔드/API

- **OpenAI API** 1.0.0+: GPT-4o-mini 모델 기반 번역 엔진
- **Python** 3.x: 메인 개발 언어

### 환경 관리

- **python-dotenv** 1.0.0+: 환경 변수 관리

### AI 모델

- **GPT-4o-mini**: 번역 성능과 비용 효율성의 균형

## 문제 해결

### API 키 오류

**증상**: "OpenAI API 키를 입력해주세요." 경고 메시지

**해결 방법**:

1. `.env` 파일이 존재하는지 확인
2. `.env` 파일에 올바른 API 키가 입력되어 있는지 확인
3. API 키 앞뒤에 공백이나 따옴표가 없는지 확인

### 번역 오류

**증상**: "번역 중 오류가 발생했습니다" 에러 메시지

**원인 및 해결 방법**:

- **API 한도 초과**: OpenAI 계정의 사용량 한도를 확인하세요
- **네트워크 연결**: 인터넷 연결 상태를 확인하세요
- **API 키 유효성**: API 키가 유효하고 활성화되어 있는지 확인하세요

### 의존성 설치 오류

**증상**: `pip install` 실행 시 오류 발생

**해결 방법**:

```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 재설치
pip install --upgrade pip
pip install -r requirements.txt
```

## 향후 계획

### Phase 2

- [ ] 번역 히스토리 저장 기능
- [ ] 즐겨찾기 기능
- [ ] 다양한 AI 모델 선택 옵션
- [ ] 번역 결과 복사 버튼

### Phase 3

- [ ] 파일 업로드를 통한 일괄 번역
- [ ] 다국어 지원 확장 (중국어, 일본어 등)
- [ ] 번역 스타일 선택 (격식체/비격식체)
- [ ] REST API 제공

자세한 내용은 [PRD.md](PRD.md)를 참고하세요.

## 기여하기

이 프로젝트에 기여하고 싶으시다면 다음 절차를 따라주세요:

1. Fork 하기
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따라주세요.

## 개발 가이드

개발자를 위한 자세한 가이드는 [CLAUDE.md](CLAUDE.md)를 참고하세요.

- 코딩 컨벤션
- 개발 가이드라인
- 문제 해결 가이드
- Claude와의 협업 팁

## 관련 문서

- [PRD.md](PRD.md) - 제품 요구사항 문서
- [CLAUDE.md](CLAUDE.md) - Claude AI 작업 가이드

## 라이선스

이 프로젝트는 개인 학습 및 개발 목적으로 작성되었습니다.

## 지원

문제가 발생하거나 질문이 있으시면 Issue를 생성해주세요.

---

**Made with ❤️ by TransBot Team**

**Last Updated**: 2026-01-22
