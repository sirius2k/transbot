# Azure Deployment 매핑 가이드

Azure OpenAI는 "deployment" 개념을 사용합니다. Deployment는 Azure Portal에서 생성한 모델 인스턴스입니다.

## Deployment 이해하기

### AZURE_DEPLOYMENTS 환경 변수 형식

```bash
AZURE_DEPLOYMENTS=모델명1:deployment명1,모델명2:deployment명2
```

### 설정 예시

```bash
# Azure Portal에서 다음과 같이 deployment를 생성했다면:
# - gpt-4o 모델을 "production-gpt4o"라는 이름으로 배포
# - gpt-4o-mini 모델을 "dev-gpt4o-mini"라는 이름으로 배포

AZURE_DEPLOYMENTS=gpt-4o:production-gpt4o,gpt-4o-mini:dev-gpt4o-mini
```

## 코드에서 파싱 결과

```python
config = Config.load()
deployments = config.parse_azure_deployments(config.AZURE_DEPLOYMENTS)
# {
#     "gpt-4o": "production-gpt4o",
#     "gpt-4o-mini": "dev-gpt4o-mini"
# }
```

## Azure 테스트 작성

Azure 기능을 테스트할 때는 Mock 객체를 사용합니다:

```python
from unittest.mock import Mock, patch

def test_azure_translation_manager():
    """Azure TranslationManager 테스트"""
    # Mock 클라이언트 생성
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "번역 결과"
    mock_client.chat.completions.create.return_value = mock_response

    # AzureTranslationManager 생성
    manager = AzureTranslationManager(
        client=mock_client,
        deployment="test-deployment"
    )

    # 번역 실행
    result = manager.translate("Hello", "English", "Korean")

    # 검증
    assert result == "번역 결과"
    mock_client.chat.completions.create.assert_called_once()
    # Azure는 deployment 이름을 model 파라미터로 사용
    call_args = mock_client.chat.completions.create.call_args
    assert call_args.kwargs["model"] == "test-deployment"
```

## Azure 개발 체크리스트

새로운 Azure 기능 추가 시 확인 사항:

- [ ] Config에 필요한 환경 변수 추가
- [ ] Config._validate_* 메서드로 검증 로직 구현
- [ ] .env.example에 설정 예시 및 설명 추가
- [ ] AzureTranslationManager에 기능 구현
- [ ] setup_api_client()에 Azure 분기 추가
- [ ] setup_sidebar()에 Deployment 표시 로직 추가
- [ ] 단위 테스트 작성 (Mock 사용)
- [ ] 에러 메시지가 사용자 친화적인지 확인
- [ ] README.md와 CLAUDE.md 문서 업데이트

---

마지막 업데이트: 2026-01-31
