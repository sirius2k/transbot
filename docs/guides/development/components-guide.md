# 컴포넌트 모듈 개발 가이드

TransBot의 컴포넌트 모듈은 클래스 기반으로 설계되어 있으며, 각 컴포넌트는 명확한 책임을 가지고 있습니다.

## 모듈 구성 원칙

### components/language.py

- **LanguageDetector 클래스**: 언어 자동 감지, 번역 방향 결정
- 언어별 설정을 딕셔너리로 관리 (DIRECTION_CONFIG)

### components/text.py

- **TextAnalyzer 클래스**: 토큰 카운팅, 문자 수 계산, Markdown 처리
- 통계 정보 생성 및 UI 표시 로직 캡슐화

### components/translation.py

- **TranslationManager 클래스**: OpenAI 클라이언트 관리, 번역 실행
- 모델 및 temperature 설정 관리
- Azure OpenAI 지원 확장 준비

## 클래스 설계 예시

```python
class LanguageDetector:
    """텍스트의 언어를 자동 감지하고 번역 방향을 결정하는 클래스"""

    # 클래스 상수: 언어별 설정을 딕셔너리로 관리
    DIRECTION_CONFIG = {
        "Korean": {
            "source": "Korean",
            "target": "English",
            "arrow": "🇰🇷 → 🇺🇸",
            "code": "ko",
            "flag": "🇰🇷"
        },
        # ... 다른 언어 설정
    }

    def __init__(self, threshold: float = 0.5):
        """초기화 메서드: 필요한 설정값 저장"""
        self.threshold = threshold

    def get_translation_direction(self, text: str) -> tuple[str, str, str]:
        """번역 방향을 결정하는 핵심 메서드

        if-elif 체인을 딕셔너리 조회로 대체하여 간결성 향상
        """
        detected = self.detect(text)
        config = self.DIRECTION_CONFIG.get(detected, self.DIRECTION_CONFIG["unknown"])
        return (config["source"], config["target"], config["arrow"])
```

## 컴포넌트 사용 예시 (app.py)

```python
# 컴포넌트 import
from components.language import LanguageDetector
from components.text import TextAnalyzer
from components.translation import TranslationManager

# 인스턴스 생성
language_detector = LanguageDetector()
text_analyzer = TextAnalyzer()
translation_manager = TranslationManager(client, model="gpt-4o-mini")

# 사용 (기존 20줄 로직이 1줄로 간소화)
source_lang, target_lang, direction_arrow = language_detector.get_translation_direction(input_text)
stats_html = text_analyzer.format_statistics_display(input_text, direction_arrow)
result = translation_manager.translate(input_text, source_lang, target_lang)
```

## 파일 수정 시 주의사항

### components/ 모듈 수정 시

- 단일 책임 원칙(SRP) 준수: 각 클래스는 하나의 명확한 책임만 가짐
- 클래스에 docstring 및 모든 메서드에 상세한 설명 작성
- 타입 힌트 명시 (예: `def method(text: str) -> str:`)
- 새로운 클래스/메서드 추가 시 반드시 단위 테스트 작성
- 기존 utils.py 함수를 래핑하여 재사용
- 상태를 가진 객체는 불변성(immutability) 고려

### utils.py 수정 시

- 순수 함수(pure function)로 유지: 부작용 없이 입력에 대한 출력만 반환
- 모든 함수에 docstring 작성
- 타입 힌트 명시 (예: `def func(text: str) -> str:`)
- 새로운 함수 추가 시 반드시 단위 테스트 작성

### requirements.txt 수정 시

- 버전 명시 권장 (예: `streamlit>=1.28.0`)
- 새로운 라이브러리 추가 시 PRD.md 업데이트

## 새 기능 추가 시

1. PRD.md의 "향후 고려사항" 섹션 확인
2. 기존 코드 구조와 일관성 유지
3. 에러 처리 및 사용자 피드백 포함
4. **단위 테스트 작성 필수**
5. 테스트 통과 확인 후 커밋

---

마지막 업데이트: 2026-01-31
