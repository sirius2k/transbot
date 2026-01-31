# 코딩 컨벤션

TransBot 프로젝트의 코딩 스타일과 문서화 규칙을 정의합니다.

## Python 스타일

- **PEP 8** 스타일 가이드 준수
- 함수와 변수명: `snake_case`
- 클래스명: `PascalCase`
- 상수: `UPPER_CASE`
- 들여쓰기: 스페이스 4칸

## Docstring 작성 기준

### 기본 원칙

"What"이 명확하면 docstring 불필요, "Why"나 "How"를 설명해야 하면 docstring 필요

### Docstring 필수 케이스

- 복잡한 매개변수를 가진 함수
- 복잡한 반환 타입 (tuple, dict)
- 예외 발생 (Raises)
- 공개 API / 라이브러리 함수
- 비직관적인 동작

### Docstring 불필요 케이스

- 자명한 단순 함수 (함수명이 명확)
- 1-3줄의 간단한 로직
- Private 구현 세부사항 (`_`로 시작)

### 주석 작성 규칙

- 복잡한 로직에는 인라인 주석 추가 (단, 자기설명적 코드 우선)
- 한국어와 영어를 혼용하여 작성 가능

## 코드 예시

### 클래스 기반 컴포넌트

```python
class TranslationManager:
    """번역 작업을 관리하는 클래스

    OpenAI 클라이언트를 관리하고 번역 설정(모델, temperature)을 유지합니다.
    """

    def __init__(self, client, model: str = "gpt-4o-mini", temperature: float = 0.3):
        """
        Args:
            client: OpenAI 클라이언트 인스턴스
            model: 사용할 AI 모델 (기본 gpt-4o-mini)
            temperature: 번역 창의성 설정 (기본 0.3)
        """
        self.client = client
        self.model = model
        self.temperature = temperature

    def translate(self, text: str, source: str, target: str) -> str:
        """텍스트를 번역합니다.

        Args:
            text: 번역할 텍스트
            source: 원본 언어 (예: "Korean", "English")
            target: 대상 언어 (예: "English", "Korean")

        Returns:
            번역된 텍스트
        """
        # API 호출 로직
        pass
```

### 함수 기반 유틸리티

```python
def detect_language(text: str) -> str:
    """텍스트의 언어를 감지합니다.

    Args:
        text: 분석할 텍스트

    Returns:
        감지된 언어명 ("Korean", "English", "unknown")
    """
    # 언어 감지 로직
    pass
```

## AI 모델 선택 구현 가이드

애플리케이션은 다양한 GPT 모델을 지원합니다. 모델 선택 기능 구현 시 다음 사항을 고려하세요.

### 지원 모델

```python
model_options = {
    "GPT-4o Mini (추천 - 가성비)": "gpt-4o-mini",
    "GPT-4o (최고 품질)": "gpt-4o",
    "GPT-4 Turbo": "gpt-4-turbo",
    "GPT-4": "gpt-4",
    "GPT-3.5 Turbo (빠름)": "gpt-3.5-turbo"
}
```

### 기본 모델 설정

- **번역 작업**: GPT-4o Mini (가성비 우수, 번역 품질 높음)
- `st.selectbox`의 `index=0`으로 기본 선택 설정

### 모델별 특징

- **GPT-4o Mini**: 번역에 최적화, 빠른 응답, 낮은 비용
- **GPT-4o**: 최신 모델, 최고 품질
- **GPT-4 Turbo**: GPT-4의 빠른 버전
- **GPT-4**: 표준 고성능 모델
- **GPT-3.5 Turbo**: 가장 빠르고 저렴

## API 키 관리

- **절대 하드코딩 금지**
- `.env` 파일 사용 (Git 제외됨)
- 사이드바 입력 옵션 유지

## 참고 자료

- [PEP 8 스타일 가이드](https://pep8.org/)
- [Python 공식 문서](https://docs.python.org/3/)

---

마지막 업데이트: 2026-01-31
