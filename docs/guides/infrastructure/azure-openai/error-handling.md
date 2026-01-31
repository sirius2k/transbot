# Azure OpenAI 에러 핸들링 가이드

Azure OpenAI 사용 시 주의할 에러 상황과 처리 방법을 안내합니다.

## 1. 필수 파라미터 누락

### 에러 시나리오

Azure provider를 선택했지만 필수 환경 변수가 설정되지 않은 경우

### 처리 방법

`app.py`의 `setup_api_client()`에서 검증:

```python
if provider == "azure":
    if not config.AZURE_OPENAI_API_KEY:
        st.error("⚠️ AZURE_OPENAI_API_KEY가 설정되지 않았습니다.")
        st.stop()
    if not config.AZURE_OPENAI_ENDPOINT:
        st.error("⚠️ AZURE_OPENAI_ENDPOINT가 설정되지 않았습니다.")
        st.stop()
```

## 2. Deployment 미설정

### 에러 시나리오

AZURE_DEPLOYMENTS 환경 변수가 없거나 비어있는 경우

### 처리 방법

`setup_sidebar()`에서 검증:

```python
if not deployments:
    st.sidebar.error("⚠️ Azure deployment가 설정되지 않았습니다.")
    st.sidebar.info("AZURE_DEPLOYMENTS 환경 변수를 설정해주세요.")
    st.stop()
```

## 3. 잘못된 Provider

### 에러 시나리오

지원하지 않는 Provider 값이 설정된 경우

### 처리 방법

`config.py`에서 검증:

```python
if provider not in ["openai", "azure"]:
    raise ValueError(f"지원하지 않는 Provider입니다: {provider}")
```

## 에러 메시지 작성 가이드

### 사용자 친화적인 에러 메시지 원칙

1. **명확한 문제 설명**: 무엇이 잘못되었는지 명확히 설명
2. **해결 방법 제시**: 사용자가 취해야 할 조치 안내
3. **이모지 활용**: ⚠️, ℹ️ 등으로 시각적 강조

### 좋은 예시

```python
st.error("⚠️ AZURE_OPENAI_API_KEY가 설정되지 않았습니다.")
st.info("💡 .env 파일에 AZURE_OPENAI_API_KEY를 추가해주세요.")
```

### 나쁜 예시

```python
st.error("Error: Missing key")  # 너무 모호함
st.error("AZURE_OPENAI_API_KEY is None")  # 기술적 용어 사용
```

## 에러 로깅

### 개발 환경

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = translation_manager.translate(text, source, target)
except Exception as e:
    logger.error(f"Translation failed: {str(e)}", exc_info=True)
    st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
```

### 프로덕션 환경

- 민감한 정보(API 키 등)는 로그에 포함하지 않기
- 스택 트레이스는 개발 환경에서만 출력
- 사용자에게는 간단하고 명확한 메시지만 표시

---

마지막 업데이트: 2026-01-31
