# TransBot 테스트 가이드

## 테스트 실행 방법

### 1. 개발 의존성 설치

```bash
pip install -r requirements-dev.txt
```

### 2. 모든 테스트 실행

```bash
pytest
```

### 3. 커버리지 리포트와 함께 테스트 실행

```bash
pytest --cov=utils --cov-report=html --cov-report=term-missing
```

### 4. HTML 리포트 확인

#### 커버리지 리포트

```bash
open htmlcov/index.html
```

#### pytest 테스트 결과 리포트

```bash
open pytest-report.html
```

## 테스트 구조

```text
tests/
├── __init__.py
├── test_utils.py          # utils.py의 핵심 함수 테스트
└── README.md              # 본 문서
```

## 테스트 커버리지 목표

- **최소 커버리지**: 80%
- **현재 커버리지**: 94.29%

## 작성된 테스트

### TestDetectLanguage (언어 감지)

- 한국어/영어 텍스트 감지
- 혼합 텍스트 감지
- 빈 문자열 및 엣지 케이스

### TestCountTokens (토큰 카운트)

- 영어/한국어 텍스트
- 다양한 AI 모델
- 긴 텍스트 처리

### TestStripMarkdown (Markdown 제거)

- 볼드, 이탤릭, 헤딩
- 링크, 이미지, 코드
- 리스트, 인용문, 수평선

### TestTranslate (번역)

- Mock을 사용한 API 호출 테스트
- 파라미터 검증
- Markdown 보존 지시 확인

## CI/CD 통합

GitHub Actions나 다른 CI/CD 도구에서 다음 명령어를 사용할 수 있습니다:

```bash
pytest --cov=utils --cov-fail-under=80
```

커버리지가 80% 미만이면 빌드가 실패합니다.

## 새로운 기능 추가 시

1. `utils.py`에 새 함수 추가
2. `tests/test_utils.py`에 해당 함수의 테스트 추가
3. 테스트 실행 및 커버리지 확인
4. 커버리지 80% 이상 유지
