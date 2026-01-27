# FEATURE-008: Azure OpenAI Service 지원

## 개요

- **기능명**: Azure OpenAI Service 지원
- **상태**: 🔲 계획 중
- **분류**: 백엔드 + 프론트엔드
- **우선순위**: P1

## 기능 설명

사용자가 OpenAI와 Azure OpenAI Service 중 선택하여 번역 서비스를 이용할 수 있도록 지원합니다. 설정 파일(.env)에서 Provider를 선택하고, 각 Provider별 필수 설정을 관리합니다.

## 배경 및 필요성

### 현재 문제점

- OpenAI API만 지원하여 Azure OpenAI Service 사용자 지원 불가
- 기업 환경에서 Azure OpenAI Service 사용 시 별도 코드 수정 필요
- Provider 전환 시 코드 변경 필요

### 기대 효과

- 기업 환경(Azure) 사용자 지원
- OpenAI와 Azure 간 유연한 전환 가능
- 하위 호환성 유지 (기존 OpenAI 사용자 영향 없음)

## 요구사항

### 기능 요구사항

| ID | 요구사항 | 우선순위 |
| -- | -------- | -------- |
| FR-1 | OpenAI와 Azure OpenAI 중 Provider 선택 | P0 |
| FR-2 | 설정 파일(.env)에서 Provider 설정 | P0 |
| FR-3 | Azure OpenAI 필수 파라미터 지원 (endpoint, api-version, deployment) | P0 |
| FR-4 | UI에서 Provider 선택 가능 (환경변수 미설정 시) | P1 |
| FR-5 | Provider에 따른 모델/Deployment 목록 분리 | P1 |

### 비기능 요구사항

| ID | 요구사항 | 설명 |
| -- | -------- | ---- |
| NFR-1 | 하위 호환성 | 기존 OpenAI 사용자 경험 유지 |
| NFR-2 | 코드 변경 최소화 | Azure 전환 시 코드 수정 불필요 |
| NFR-3 | 명확한 에러 메시지 | Provider 설정 오류 시 상세한 안내 |

## 작업(Task) 분해

### Task 8.1: 환경 변수 설정 추가

- **분류**: 백엔드 (설정)
- **의존성**: 없음
- **작업 내용**:
  - `.env.example`에 Provider 선택 변수 추가
    - `AI_PROVIDER` (openai/azure)
  - Azure OpenAI 관련 환경 변수 추가
    - `AZURE_OPENAI_API_KEY`
    - `AZURE_OPENAI_ENDPOINT`
    - `AZURE_OPENAI_API_VERSION`
    - `AZURE_DEPLOYMENTS` (모델명:deployment명 매핑)
- **예상 파일**: `.env.example`
- **예상 소요 시간**: 30분

### Task 8.2: 클라이언트 생성 로직 구현

- **분류**: 백엔드
- **의존성**: Task 8.1
- **작업 내용**:
  - `utils.py`에 `create_client()` 함수 추가
    - Provider에 따라 OpenAI/AzureOpenAI 클라이언트 생성
    - Azure 필수 파라미터 검증
  - `parse_azure_deployments()` 함수 추가
    - 환경 변수의 deployment 문자열 파싱
    - UI 표시용 모델명 매핑
- **예상 파일**: `utils.py`
- **예상 소요 시간**: 1시간

### Task 8.3: app.py Provider 선택 로직

- **분류**: 백엔드 + 프론트엔드
- **의존성**: Task 8.1, Task 8.2
- **작업 내용**:
  - 환경 변수에서 Provider 로드
  - Provider별 클라이언트 생성 분기
  - OpenAI/Azure 각각의 API 키 및 설정 관리
- **예상 파일**: `app.py` (클라이언트 생성 섹션)
- **예상 소요 시간**: 1시간

### Task 8.4: UI에서 Provider 선택 기능

- **분류**: 프론트엔드
- **의존성**: Task 8.3
- **작업 내용**:
  - 사이드바에 Provider 선택 추가 (환경변수 미설정 시)
  - Azure 선택 시 추가 입력 필드 표시
    - Endpoint 입력
    - API Version 입력 (기본값 제공)
  - Provider 정보 표시 (헤더에 OpenAI/Azure 표시)
- **예상 파일**: `app.py` (사이드바 섹션)
- **예상 소요 시간**: 1시간

### Task 8.5: 모델/Deployment 목록 관리

- **분류**: 백엔드 + 프론트엔드
- **의존성**: Task 8.2, Task 8.4
- **작업 내용**:
  - Provider에 따른 모델 목록 분리
    - OpenAI: 기존 모델 목록
    - Azure: 환경변수에서 로드한 deployment 목록
  - Deployment 미설정 시 경고 메시지 표시
  - 모델/Deployment 선택 UI 라벨 변경
- **예상 파일**: `app.py` (모델 선택 섹션)
- **예상 소요 시간**: 30분

### Task 8.6: 에러 핸들링 및 검증

- **분류**: 백엔드 + 프론트엔드
- **의존성**: Task 8.1 ~ Task 8.5
- **작업 내용**:
  - Azure 필수 파라미터 누락 시 명확한 에러 메시지
  - Provider 설정 오류 시 안내 메시지
  - API 호출 실패 시 Provider별 에러 처리
- **예상 파일**: `utils.py`, `app.py`
- **예상 소요 시간**: 30분

### Task 8.7: 단위 테스트 작성

- **분류**: 테스트
- **의존성**: Task 8.2, Task 8.6
- **작업 내용**:
  - `create_client()` 함수 테스트
    - OpenAI 클라이언트 생성 테스트
    - Azure 클라이언트 생성 테스트
    - 필수 파라미터 누락 시 에러 테스트
  - `parse_azure_deployments()` 함수 테스트
    - 정상 파싱 테스트
    - 빈 문자열 처리 테스트
- **예상 파일**: `tests/test_utils.py`
- **예상 소요 시간**: 1시간

### Task 8.8: 문서 업데이트

- **분류**: 문서
- **의존성**: Task 8.1 ~ Task 8.7
- **작업 내용**:
  - README.md: Azure OpenAI 설정 가이드 추가
  - CLAUDE.md: Azure OpenAI 개발 가이드 추가
  - PRD.md: 완료된 기능에 Azure 지원 추가
- **예상 파일**: `README.md`, `CLAUDE.md`, `PRD.md`
- **예상 소요 시간**: 1시간

## 작업 흐름도

```text
Task 8.1 (환경변수 설정)
    │
    ├──→ Task 8.2 (클라이언트 생성 로직)
    │       │
    │       ├──→ Task 8.3 (Provider 선택)
    │       │       │
    │       │       └──→ Task 8.4 (UI Provider 선택)
    │       │               │
    │       │               └──→ Task 8.5 (모델/Deployment 목록)
    │       │
    │       └──→ Task 8.7 (단위 테스트)
    │
    └──→ Task 8.6 (에러 핸들링)
            │
            └──→ Task 8.8 (문서 업데이트)
```

## 기술 분석

### OpenAI vs Azure OpenAI 차이점

| 항목 | OpenAI | Azure OpenAI |
| ---- | ------ | ------------ |
| 클라이언트 클래스 | `OpenAI` | `AzureOpenAI` |
| 필수 파라미터 | `api_key` | `api_key`, `azure_endpoint`, `api_version` |
| 모델 지정 | 모델명 (예: gpt-4o) | Deployment 이름 (사용자 정의) |
| 엔드포인트 | 고정 (api.openai.com) | 사용자 리소스 URL |

### Azure OpenAI 클라이언트 예시

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-azure-api-key",
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_version="2024-02-15-preview"
)

response = client.chat.completions.create(
    model="your-gpt4-deployment",  # Deployment 이름
    messages=[...]
)
```

## 완료 기준

- [ ] `.env.example`에 모든 Azure 관련 변수 추가됨
- [ ] OpenAI Provider로 정상 번역 동작
- [ ] Azure Provider로 정상 번역 동작
- [ ] Provider 전환 시 코드 수정 없이 동작
- [ ] Azure 필수 파라미터 누락 시 명확한 에러 메시지
- [ ] 환경변수 미설정 시 UI에서 Provider 선택 가능
- [ ] 모든 단위 테스트 통과
- [ ] 문서 업데이트 완료 (README, CLAUDE, PRD)

## 테스트 계획

### 테스트 케이스

| ID | 테스트 시나리오 | 예상 결과 |
| -- | --------------- | --------- |
| TC-1 | AI_PROVIDER=openai 설정 | OpenAI 클라이언트 생성 성공 |
| TC-2 | AI_PROVIDER=azure + 모든 필수 변수 설정 | AzureOpenAI 클라이언트 생성 성공 |
| TC-3 | AI_PROVIDER=azure + 변수 누락 | 명확한 에러 메시지 표시 |
| TC-4 | AI_PROVIDER 미설정 | UI에서 Provider 선택 가능 |
| TC-5 | OpenAI로 번역 실행 | 정상 번역 완료 |
| TC-6 | Azure로 번역 실행 | 정상 번역 완료 |
| TC-7 | Provider 전환 (OpenAI ↔ Azure) | .env만 수정으로 전환 성공 |
| TC-8 | Azure Deployment 미설정 | 경고 메시지 표시 |

### 단위 테스트

```python
# tests/test_utils.py

def test_create_client_openai():
    """OpenAI 클라이언트 생성 테스트"""
    client = create_client(provider="openai", api_key="test-key")
    assert isinstance(client, OpenAI)

def test_create_client_azure():
    """Azure OpenAI 클라이언트 생성 테스트"""
    client = create_client(
        provider="azure",
        api_key="test-key",
        azure_endpoint="https://test.openai.azure.com/",
        api_version="2024-02-15-preview"
    )
    assert isinstance(client, AzureOpenAI)

def test_create_client_azure_missing_params():
    """Azure 필수 파라미터 누락 시 에러 테스트"""
    with pytest.raises(ValueError):
        create_client(provider="azure", api_key="test-key")

def test_parse_azure_deployments():
    """Azure deployment 파싱 테스트"""
    deployments_str = "gpt-4o:my-gpt4o,gpt-4o-mini:my-mini"
    result = parse_azure_deployments(deployments_str)
    assert "GPT-4o" in result
    assert result["GPT-4o"] == "my-gpt4o"
```

## 리스크 및 고려사항

| 리스크 | 영향도 | 대응 방안 |
| ------ | ------ | --------- |
| Azure API 버전 변경 | 중 | api_version을 환경변수로 관리 |
| Deployment 이름 오타 | 중 | 명확한 에러 메시지 제공 |
| 하위 호환성 깨짐 | 높 | 기존 OpenAI 사용자 경험 유지 필수 |
| 문서 미흡 | 중 | Azure 설정 가이드 상세 작성 |

## 참고 자료

- [Azure OpenAI Service 공식 문서](https://learn.microsoft.com/azure/ai-services/openai/)
- [OpenAI Python SDK - Azure OpenAI](https://github.com/openai/openai-python#microsoft-azure-openai)
- [Azure OpenAI API Reference](https://learn.microsoft.com/azure/ai-services/openai/reference)

---

**작성일**: 2026년 1월 27일
**작성자**: TransBot Development Team
