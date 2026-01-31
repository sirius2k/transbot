# Azure OpenAI 설정 가이드

TransBot은 OpenAI API와 Azure OpenAI Service를 모두 지원합니다. Azure OpenAI를 사용하면 Microsoft Azure 인프라에서 OpenAI 모델을 사용할 수 있습니다.

## Azure vs OpenAI 비교

| 항목 | OpenAI API | Azure OpenAI Service |
| ------ | ------------ | --------------------- |
| **API 키** | `OPENAI_API_KEY` | `AZURE_OPENAI_API_KEY` |
| **엔드포인트** | 고정 (api.openai.com) | 사용자 지정 (Azure Portal) |
| **모델 지정** | 모델 이름 (예: gpt-4o) | Deployment 이름 (사용자 정의) |
| **설정 방식** | 직접 모델 선택 | Deployment 매핑 필요 |
| **클라이언트** | `OpenAI()` | `AzureOpenAI()` |

## 환경 변수 설정

`.env` 파일에 다음 설정을 추가합니다:

```bash
# Provider 선택
AI_PROVIDER=azure

# Azure 필수 설정
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Deployment 매핑
AZURE_DEPLOYMENTS=gpt-4o:my-gpt4o-deployment,gpt-4o-mini:my-mini-deployment
```

## Config 클래스에서 로드

```python
from config import Config

config = Config.load()
print(config.AI_PROVIDER)  # "azure"
print(config.AZURE_OPENAI_API_KEY)  # Azure API 키
print(config.parse_azure_deployments(config.AZURE_DEPLOYMENTS))
# {'gpt-4o': 'my-gpt4o-deployment', 'gpt-4o-mini': 'my-mini-deployment'}
```

## Azure TranslationManager 사용

Azure를 사용할 때는 `AzureTranslationManager` 클래스가 자동으로 사용됩니다.

```python
from components.translation import TranslationManagerFactory, AzureTranslationManager
from openai import AzureOpenAI
from config import Config

# Config 로드
config = Config.load()

# Azure deployment 목록 로드
AzureTranslationManager.load_deployments(config)

# Azure 클라이언트 생성
client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_API_KEY,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_version=config.AZURE_OPENAI_API_VERSION
)

# Factory로 TranslationManager 생성
translation_manager = TranslationManagerFactory.create(
    provider="azure",
    client=client,
    deployment="my-gpt4o-deployment"  # Azure는 deployment 이름 필수
)

# 번역 실행
result = translation_manager.translate("Hello", "English", "Korean")
```

## setup_sidebar()에서 Deployment 표시

Azure provider 사용 시 사이드바는 deployment 목록을 표시합니다:

```python
def setup_sidebar(provider: str) -> tuple[str, dict[str, str]]:
    if provider == "azure":
        from components.translation import AzureTranslationManager
        deployments = AzureTranslationManager.SUPPORTED_DEPLOYMENTS

        # Deployment가 없으면 에러
        if not deployments:
            st.error("⚠️ Azure deployment가 설정되지 않았습니다.")
            st.stop()

        # Deployment 옵션 생성
        deployment_options = {
            f"{model} (Azure)": deployment
            for model, deployment in deployments.items()
        }

        # Selectbox로 deployment 선택
        selected_name = st.sidebar.selectbox(
            "Azure Deployment 선택:",
            options=list(deployment_options.keys())
        )
        return deployment_options[selected_name], deployment_options
```

## 참고 자료

- [Deployment 매핑 가이드](deployment.md)
- [에러 핸들링 가이드](error-handling.md)

---

마지막 업데이트: 2026-01-31
