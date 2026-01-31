# 테스트 가이드

TransBot 프로젝트의 테스트 작성 및 실행 가이드입니다.

## 테스트 작성 원칙

### 1. 단위 테스트 작성 규칙

- 모든 핵심 함수는 반드시 테스트 작성
- 테스트 파일명: `test_[모듈명].py` (예: `test_utils.py`)
- 테스트 클래스명: `Test[기능명]` (예: `TestDetectLanguage`)
- 테스트 함수명: `test_[테스트내용]` (예: `test_detect_korean`)

### 2. 테스트 케이스 작성 가이드

```python
class TestDetectLanguage:
    """언어 감지 함수 테스트"""

    def test_detect_korean(self):
        """한국어 텍스트 감지 테스트"""
        result = detect_language("안녕하세요")
        assert result == "Korean"
```

### 3. Mock 객체 사용

외부 API 호출이 필요한 함수는 Mock 객체를 사용하여 테스트합니다.

```python
from unittest.mock import Mock

def test_translate_success():
    """번역 성공 테스트"""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "번역된 텍스트"

    mock_client.chat.completions.create.return_value = mock_response

    result = translate(mock_client, "Hello", "English", "Korean", "gpt-4o")
    assert result == "번역된 텍스트"
```

## 테스트 실행

### 기본 실행 명령어

```bash
# 모든 테스트 실행
pytest

# 특정 파일 테스트
pytest tests/test_utils.py

# 특정 클래스 테스트
pytest tests/test_utils.py::TestDetectLanguage

# 특정 함수 테스트
pytest tests/test_utils.py::TestDetectLanguage::test_detect_korean

# 상세 출력
pytest -v

# 커버리지와 함께 실행
pytest --cov=utils --cov-report=html
```

## 테스트 커버리지 확인

```bash
# 터미널에서 커버리지 확인
pytest --cov=utils --cov-report=term-missing

# HTML 리포트 생성
pytest --cov=utils --cov-report=html

# 리포트 열기 (macOS)
open htmlcov/index.html

# 리포트 열기 (Linux)
xdg-open htmlcov/index.html

# 리포트 열기 (Windows)
start htmlcov/index.html
```

## 커버리지 목표

- **최소 커버리지**: 80% 이상 유지
- **현재 커버리지**: 97.98% 달성 (2026-01-27 기준)
- **핵심 함수**: 100% 커버리지 목표
- 커버리지 80% 미만 시 pytest 실패 (`pytest.ini`에 설정됨)

## 테스트 현황

### 전체 테스트 통계 (2026-01-27 기준)

- **총 테스트 수**: 79개
- **전체 커버리지**: 97.98%
- **모듈별 커버리지**: 모든 컴포넌트 100% 달성

### 모듈별 테스트 세부사항

#### utils.py (32개 테스트)

- `detect_language()`: 언어 감지 함수 (8개 테스트)
- `count_tokens()`: 토큰 카운팅 함수 (5개 테스트)
- `strip_markdown()`: Markdown 제거 함수 (14개 테스트)
- `translate()`: 번역 함수 (3개 Mock 테스트)
- 기타 유틸리티 함수 (2개 테스트)

#### components/language.py (16개 테스트)

- `LanguageDetector.detect()`: 언어 감지 메서드
- `LanguageDetector.get_translation_direction()`: 번역 방향 결정
- `LanguageDetector.get_language_code()`: 언어 코드 변환
- `LanguageDetector.get_language_flag()`: 플래그 이모지 반환

#### components/text.py (16개 테스트)

- `TextAnalyzer.count_tokens()`: 토큰 카운팅
- `TextAnalyzer.get_statistics()`: 통계 정보 생성
- `TextAnalyzer.strip_markdown()`: Markdown 제거
- `TextAnalyzer.has_markdown()`: Markdown 포함 여부 확인
- `TextAnalyzer.format_statistics_display()`: UI 표시용 HTML 생성

#### components/translation.py (15개 테스트)

- `TranslationManager.translate()`: 번역 수행
- `TranslationManager.set_model()`: 모델 변경
- `TranslationManager.set_temperature()`: temperature 설정
- `TranslationManager.validate_model()`: 모델 검증
- `TranslationManager.get_model_list()`: 지원 모델 목록 조회

## 컴포넌트 테스트 작성 가이드

### 클래스 테스트 구조

```python
class TestLanguageDetector:
    """LanguageDetector 클래스 테스트"""

    def test_detect_korean(self):
        """한국어 텍스트 감지 테스트"""
        detector = LanguageDetector()
        result = detector.detect("안녕하세요")
        assert result == "Korean"

    def test_get_translation_direction_korean(self):
        """한국어 번역 방향 결정 테스트"""
        detector = LanguageDetector()
        source, target, arrow = detector.get_translation_direction("안녕하세요")
        assert source == "Korean"
        assert target == "English"
        assert arrow == "🇰🇷 → 🇺🇸"
```

### 컴포넌트 테스트 작성 원칙

1. **각 컴포넌트마다 별도의 테스트 파일 작성**
   - `test_language.py`, `test_text.py`, `test_translation.py`

2. **클래스별 테스트 클래스 생성**
   - 테스트 클래스명: `Test[클래스명]` (예: `TestLanguageDetector`)

3. **메서드별 테스트 함수 작성**
   - 테스트 함수명: `test_[메서드명]_[시나리오]` (예: `test_detect_korean`)

4. **경계값 및 예외 상황 테스트**
   - 정상 케이스, 에러 케이스, 엣지 케이스 모두 커버

5. **Mock 객체 활용**
   - 외부 API 의존성은 Mock으로 대체하여 테스트

## 배포 체크리스트 (테스트 및 품질)

- [ ] **모든 단위 테스트 통과 확인** (`pytest`)
- [ ] **코드 커버리지 80% 이상 확인** (`pytest --cov`)
- [ ] 테스트 리포트 생성 확인 (`htmlcov/`)
- [ ] 새로운 함수에 대한 테스트 작성 완료

---

마지막 업데이트: 2026-01-31
