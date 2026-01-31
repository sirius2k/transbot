# 설정 관리 개발 가이드

TransBot은 환경 변수 기반 설정 관리 시스템을 사용합니다.

## Config 클래스 설계 원칙

모든 설정은 `.env` 파일 또는 환경 변수로 관리되며, 설정되지 않은 값은 기본값이 사용됩니다.

### 주요 특징

- **12-factor app 원칙**: 설정과 코드 분리
- **타입 안전성**: 환경 변수를 적절한 타입으로 변환 및 검증
- **기본값 제공**: 모든 설정에 합리적인 기본값 존재
- **검증 메커니즘**: 잘못된 설정값 사용 방지

## Config 클래스 사용 방법

```python
from config import Config

# 설정 로드
config = Config.load()

# 설정값 사용
print(config.DEFAULT_MODEL)        # "gpt-4o-mini"
print(config.APP_TITLE)            # "영어-한국어 번역기"
print(config.MAX_INPUT_LENGTH)     # 50000
```

## 새로운 설정 추가 방법

### 1. config.py에 기본값 정의

```python
class Config:
    # 기본값 정의
    _DEFAULT_NEW_SETTING = "default_value"

    def __init__(self):
        self.NEW_SETTING: str = self._DEFAULT_NEW_SETTING
```

### 2. load() 메서드에 로딩 로직 추가

```python
@classmethod
def load(cls) -> 'Config':
    config = cls()

    # 환경 변수에서 로드
    config.NEW_SETTING = cls._get_str_env(
        "NEW_SETTING",
        cls._DEFAULT_NEW_SETTING
    )

    # 필요시 검증
    cls._validate_new_setting(config.NEW_SETTING)

    return config
```

### 3. 필요시 검증 메서드 추가

```python
@staticmethod
def _validate_new_setting(value: str) -> None:
    """새 설정 검증"""
    if value not in ["option1", "option2"]:
        raise ValueError(f"유효하지 않은 설정: {value}")
```

### 4. .env.example 업데이트

```bash
# 새로운 설정 설명
# 기본값: default_value
# NEW_SETTING=default_value
```

### 5. 단위 테스트 작성

`tests/test_config.py`에 테스트 추가:

```python
def test_load_new_setting(self, monkeypatch):
    """새 설정 로드 테스트"""
    monkeypatch.setenv("NEW_SETTING", "custom_value")
    config = Config.load()
    assert config.NEW_SETTING == "custom_value"

def test_validate_new_setting_invalid(self):
    """새 설정 검증 실패 테스트"""
    with pytest.raises(ValueError):
        Config._validate_new_setting("invalid_value")
```

## 타입별 환경 변수 로드 메서드

```python
# 문자열
config.STR_VALUE = Config._get_str_env("KEY", "default")

# 정수
config.INT_VALUE = Config._get_int_env("KEY", 100)

# 실수
config.FLOAT_VALUE = Config._get_float_env("KEY", 0.5)
```

## 컴포넌트에서 Config 사용

```python
from config import Config

class TranslationManager:
    def __init__(self, client, model: Optional[str] = None):
        # Config에서 기본값 로드
        config = Config.load()
        self.model = model if model is not None else config.DEFAULT_MODEL
```

## 설정 관리 주의사항

1. **기본값 필수**: 모든 설정은 반드시 합리적인 기본값을 가져야 합니다
2. **타입 안전성**: 환경 변수는 항상 문자열이므로 적절한 타입 변환 필수
3. **검증 우선**: 잘못된 설정값은 애플리케이션 시작 시 즉시 감지되어야 합니다
4. **문서화**: .env.example에 설정 설명과 기본값 명시 필수
5. **테스트 커버리지**: 새로운 설정은 반드시 단위 테스트로 검증

## config.py 수정 시 주의사항

- 환경 변수 기반 설정 관리 원칙 준수
- 새로운 설정 추가 시 기본값 정의 필수
- 타입 변환 및 검증 메서드 구현
- .env.example 파일 동시 업데이트
- 단위 테스트 작성 필수

---

마지막 업데이트: 2026-01-31
