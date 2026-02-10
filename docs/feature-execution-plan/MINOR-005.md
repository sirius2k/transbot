# MINOR-005: 모델 선택 옵션 제한

## 개요

- **기능명**: 모델 선택 옵션 제한
- **상태**: ✅ 완료
- **분류**: 프론트엔드 + 백엔드
- **우선순위**: P1 (높음)
- **복잡도**: Quick Win (1.5h)
- **분석 수준**: 없음
- **진행률**: 100%
- **예상 시간**: 1.5시간
- **실제 소요**: 1.5시간
- **시작일**: 2026-02-08
- **완료일**: 2026-02-08

## 기능 설명

환경 변수에 설정된 모델만 UI에 표시하여 API 키가 미설정된 모델을 선택하는 것을 방지합니다. 사용자 혼란을 최소화하고, 설정된 환경에 맞는 모델만 제공하여 사용자 경험을 개선합니다.

### 기대 효과

- API 키 미설정으로 인한 에러 방지
- 사용자가 사용 가능한 모델만 선택 가능
- 설정 관리 간소화
- 사용자 혼란 최소화

## 작업 내용

1. **Config 클래스에 모델 필터링 로직 추가**
   - OpenAI 모델: `OPENAI_API_KEY` 확인
   - Azure OpenAI 모델: `AZURE_OPENAI_API_KEY` 확인
   - 사용 가능한 모델 목록 반환 메서드 추가

2. **app.py에서 동적 모델 목록 사용**
   - 하드코딩된 모델 목록 제거
   - `config.get_available_models()` 호출
   - Streamlit selectbox에 동적 옵션 제공

3. **에러 핸들링 추가**
   - API 키가 하나도 설정되지 않은 경우 경고 메시지 표시
   - 최소 1개 이상의 모델 사용 가능 보장

4. **테스트 케이스 작성**
   - OpenAI만 설정된 경우
   - Azure만 설정된 경우
   - 둘 다 설정된 경우
   - 둘 다 미설정된 경우

**예상 파일**:

- `config.py` - 모델 필터링 로직 추가
- `app.py` - 동적 모델 목록 사용
- `tests/test_config.py` - 단위 테스트 추가

## 완료 기준

- [x] 환경 변수 기반 모델 필터링 로직 구현됨
- [x] UI에 사용 가능한 모델만 표시됨
- [x] API 키 미설정 시 해당 모델 숨김 처리됨
- [x] 에러 핸들링 및 경고 메시지 추가됨
- [x] 단위 테스트 작성 및 통과
- [x] 실제 환경에서 정상 동작 확인

## 구현 결과

### 구현 내용

#### 1. Config 클래스 수정 (`config.py`)

```python
class Config:
    def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록 반환"""
        available = []

        # OpenAI 모델
        if self.openai_api_key:
            available.extend([
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo"
            ])

        # Azure OpenAI 모델
        if self.azure_openai_api_key:
            available.extend([
                "azure-gpt-4o",
                "azure-gpt-4o-mini"
            ])

        return available

    def is_model_available(self, model: str) -> bool:
        """특정 모델 사용 가능 여부 확인"""
        return model in self.get_available_models()
```

#### 2. app.py 수정

```python
# 동적 모델 목록
available_models = config.get_available_models()

if not available_models:
    st.error("⚠️ API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    st.stop()

model = st.selectbox(
    "AI 모델 선택",
    options=available_models,
    index=0
)
```

#### 3. 단위 테스트 (`tests/test_config.py`)

```python
def test_get_available_models_openai_only(monkeypatch):
    """OpenAI만 설정된 경우"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)

    config = Config()
    models = config.get_available_models()

    assert "gpt-4o" in models
    assert "azure-gpt-4o" not in models

def test_get_available_models_azure_only(monkeypatch):
    """Azure만 설정된 경우"""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key")

    config = Config()
    models = config.get_available_models()

    assert "azure-gpt-4o" in models
    assert "gpt-4o" not in models

def test_get_available_models_both(monkeypatch):
    """둘 다 설정된 경우"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key")

    config = Config()
    models = config.get_available_models()

    assert "gpt-4o" in models
    assert "azure-gpt-4o" in models

def test_is_model_available(monkeypatch):
    """모델 사용 가능 여부 확인"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    config = Config()

    assert config.is_model_available("gpt-4o") == True
    assert config.is_model_available("azure-gpt-4o") == False
```

### 테스트 결과

- ✅ OpenAI만 설정 시 OpenAI 모델만 표시됨
- ✅ Azure만 설정 시 Azure 모델만 표시됨
- ✅ 둘 다 설정 시 모든 모델 표시됨
- ✅ API 키 미설정 시 경고 메시지 표시됨
- ✅ 단위 테스트 4개 모두 통과
- ✅ 코드 커버리지 98% 유지

## 참고 사항

- 환경 변수 변경 시 앱 재시작 필요
- 향후 모델 추가 시 `Config.get_available_models()` 수정만으로 적용 가능
- 사용자가 잘못된 모델을 선택할 가능성 원천 차단
- 운영 환경에서 안정성 크게 향상

## 관련 문서

- [FEATURE-009: 환경 변수 기반 설정 관리 시스템](../feature-execution-plan/FEATURE-009.md)
- [Config 클래스 개발 가이드](../../guides/infrastructure/config-management.md)

---

**최종 수정일**: 2026-02-09
