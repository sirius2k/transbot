# Langfuse 사용 가이드

Langfuse 대시보드를 사용하여 TransBot의 번역 요청을 추적하고, 비용을 분석하며, 품질을 모니터링하는 방법을 설명합니다.

이 가이드는 Langfuse v2 대시보드를 기준으로 작성되었습니다.

## 개요

Langfuse 대시보드는 LLM 애플리케이션의 관찰성을 위한 웹 인터페이스를 제공합니다.

### 주요 기능

- **Traces**: 번역 요청 추적 및 입력/출력 확인
- **Sessions**: 사용자 세션별 번역 요청 그룹핑
- **Users**: 사용자별 사용량 추적
- **Prompts**: 프롬프트 버전 관리
- **Playground**: 프롬프트 테스트 및 실험
- **Settings**: API 키 및 프로젝트 설정

## Langfuse 대시보드 접속

### 로컬 개발 환경

로컬에서 자체 호스팅한 Langfuse에 접속합니다.

1. 브라우저에서 `http://localhost:3000` 접속
2. 이메일과 비밀번호로 로그인
3. 프로젝트 선택 (예: `TransBot`)

### 대시보드 레이아웃

Langfuse 대시보드는 다음과 같은 레이아웃을 가지고 있습니다:

- **왼쪽 사이드바**: 주요 메뉴 (Traces, Sessions, Users 등)
- **상단 바**: 프로젝트 선택, 사용자 설정
- **메인 영역**: 선택한 메뉴의 콘텐츠

## 추적 데이터 확인

Langfuse의 핵심 기능은 LLM 호출을 추적하고 분석하는 것입니다.

### Traces 메뉴

**Traces** 메뉴에서 TransBot의 모든 번역 요청을 확인할 수 있습니다.

1. 왼쪽 사이드바에서 **Traces** 클릭
2. 번역 요청 목록이 시간순으로 표시됨

각 Trace에는 다음 정보가 표시됩니다:

- **Name**: `translation` (번역 요청)
- **Timestamp**: 요청 시간
- **Latency**: 응답 시간 (밀리초)
- **Tokens**: 입력/출력 토큰 수
- **Cost**: 예상 비용 (USD)
- **Status**: 성공/실패 상태

### Trace 상세 정보

특정 Trace를 클릭하면 상세 정보를 확인할 수 있습니다.

#### 1. Input (입력)

번역 요청의 입력 데이터:

```json
{
  "source_text": "Hello, how are you?",
  "source_lang": "en",
  "target_lang": "ko"
}
```

- **source_text**: 원문 텍스트
- **source_lang**: 원본 언어 코드 (en: 영어, ko: 한국어)
- **target_lang**: 대상 언어 코드

#### 2. Output (출력)

번역 결과:

```json
{
  "target_text": "안녕하세요, 어떻게 지내세요?"
}
```

- **target_text**: 번역된 텍스트

#### 3. Metadata (메타데이터)

번역 요청의 추가 정보:

```json
{
  "model": "gpt-4o-mini",
  "direction": "en→ko",
  "session_id": "st_abc123",
  "latency_ms": 1234.56
}
```

- **model**: 사용된 AI 모델 (예: gpt-4o-mini, gpt-4o)
- **direction**: 번역 방향 (예: en→ko, ko→en)
- **session_id**: Streamlit 세션 ID (사용자별 세션 추적)
- **latency_ms**: 응답 시간 (밀리초)

#### 4. Usage (사용량)

토큰 사용량:

- **Input Tokens**: 입력 토큰 수 (원문 텍스트 + 프롬프트)
- **Output Tokens**: 출력 토큰 수 (번역된 텍스트)
- **Total Tokens**: 총 토큰 수

#### 5. Level (레벨)

에러 발생 여부:

- **DEFAULT**: 정상 (성공)
- **ERROR**: 에러 발생

에러 발생 시 **Status Message** 필드에 에러 메시지가 표시됩니다.

### Timeline 뷰

Trace 상세 페이지의 **Timeline** 탭에서 요청의 시간 흐름을 확인할 수 있습니다:

1. 요청 시작
2. OpenAI API 호출
3. 응답 수신
4. 요청 완료

각 단계의 소요 시간이 시각화되어 병목 지점을 파악할 수 있습니다.

## 필터 및 검색

Traces 목록에서 원하는 데이터를 찾기 위해 다양한 필터를 사용할 수 있습니다.

### 날짜 필터

상단의 날짜 선택기를 사용하여 특정 기간의 Trace를 확인합니다.

- **Last 24 hours**: 최근 24시간
- **Last 7 days**: 최근 7일
- **Last 30 days**: 최근 30일
- **Custom Range**: 사용자 정의 기간

### 세션 ID 필터

특정 사용자 세션의 번역 요청을 확인합니다.

1. Trace 목록에서 **Session ID** 열 확인
2. Session ID 클릭
3. 해당 세션의 모든 Trace 표시

### 에러 레벨 필터

에러가 발생한 Trace만 확인합니다.

1. 상단의 **Level** 드롭다운 클릭
2. **ERROR** 선택
3. 에러 레벨의 Trace만 표시

### 모델 필터

특정 AI 모델을 사용한 Trace만 확인합니다.

1. 검색창에 `metadata.model = "gpt-4o-mini"` 입력
2. 해당 모델을 사용한 Trace만 표시

### 번역 방향 필터

특정 번역 방향의 Trace만 확인합니다.

1. 검색창에 `metadata.direction = "en→ko"` 입력
2. 영어→한국어 번역만 표시

## 비용 분석

Langfuse는 토큰 사용량을 기반으로 예상 비용을 계산합니다.

### Dashboard 메뉴

왼쪽 사이드바에서 **Dashboard** 클릭하면 다음 정보를 확인할 수 있습니다:

- **Total Traces**: 총 Trace 수
- **Total Tokens**: 총 토큰 사용량
- **Estimated Cost**: 예상 총 비용 (USD)
- **Average Latency**: 평균 응답 시간

### 비용 차트

시간별, 일별 비용 추이를 차트로 확인할 수 있습니다:

- **Line Chart**: 시간 흐름에 따른 비용 변화
- **Bar Chart**: 일별 토큰 사용량 및 비용

### 모델별 비용 비교

다양한 AI 모델의 비용을 비교합니다:

1. Dashboard에서 **Model** 필터 적용
2. 모델별 토큰 사용량 및 비용 확인
3. 가장 비용 효율적인 모델 선택

**예시**:

| 모델 | 총 토큰 | 예상 비용 | 평균 응답 시간 |
| --- | --- | --- | --- |
| gpt-4o-mini | 100,000 | $0.15 | 1.2s |
| gpt-4o | 50,000 | $2.50 | 1.8s |
| gpt-4-turbo | 30,000 | $0.90 | 1.0s |

> **팁**: gpt-4o-mini는 가장 비용 효율적이면서도 번역 품질이 우수합니다.

## Sessions (세션 추적)

TransBot은 Streamlit 세션 ID를 Langfuse에 전송하여 사용자별 번역 요청을 그룹핑합니다.

### Sessions 메뉴

왼쪽 사이드바에서 **Sessions** 클릭하면 세션 목록이 표시됩니다.

각 세션에는 다음 정보가 표시됩니다:

- **Session ID**: Streamlit 세션 ID (예: `st_abc123`)
- **Traces**: 해당 세션의 Trace 수
- **Tokens**: 총 토큰 사용량
- **Cost**: 예상 비용
- **First Seen**: 최초 요청 시간
- **Last Seen**: 최근 요청 시간

### 세션 상세 정보

특정 세션을 클릭하면 해당 세션의 모든 Trace를 시간순으로 확인할 수 있습니다.

**사용 예시**:

- 특정 사용자가 어떤 텍스트를 번역했는지 추적
- 사용자별 번역 품질 분석
- 사용자별 비용 산출

## Prompts (프롬프트 관리)

Langfuse는 프롬프트 버전 관리 기능을 제공하지만, TransBot은 현재 이 기능을 사용하지 않습니다.

### 향후 계획

TransBot이 프롬프트 버전 관리를 도입하면 다음과 같은 이점이 있습니다:

- 프롬프트 변경 이력 추적
- A/B 테스트를 통한 프롬프트 최적화
- 프롬프트 성능 비교 (품질, 비용, 응답 시간)

## 유용한 팁

### 1. 에러 추적

에러가 발생한 번역 요청을 빠르게 찾으려면:

1. Traces 메뉴에서 **Level** 필터를 **ERROR**로 설정
2. 에러 메시지를 확인하여 문제 원인 파악
3. 입력 텍스트를 확인하여 재현 테스트

### 2. 성능 모니터링

번역 응답 시간이 느린 경우:

1. Traces 목록을 **Latency** 기준으로 정렬
2. 응답 시간이 긴 Trace 확인
3. 입력 텍스트 길이와 응답 시간의 상관관계 분석
4. 필요시 더 빠른 모델(gpt-4-turbo)로 전환

### 3. 비용 최적화

비용을 절감하려면:

1. Dashboard에서 모델별 비용 비교
2. gpt-4o-mini 사용 (가성비 우수)
3. 불필요한 번역 요청 최소화
4. 캐싱 활용 (동일 텍스트 재번역 방지)

### 4. 품질 모니터링

번역 품질을 확인하려면:

1. 무작위로 Trace 샘플링
2. 입력(원문)과 출력(번역) 비교
3. 번역 품질이 낮은 경우 모델 변경 (gpt-4o 사용)
4. 프롬프트 개선 (향후 버전 관리 기능 사용)

### 5. 데이터 내보내기

Langfuse 데이터를 외부로 내보내려면:

1. Settings > Data Export 메뉴
2. CSV 또는 JSON 형식 선택
3. 날짜 범위 지정
4. Export 버튼 클릭

내보낸 데이터는 다음과 같은 용도로 사용할 수 있습니다:

- 사용자 보고서 생성
- 비용 정산
- 데이터 분석 (Jupyter Notebook, Excel 등)

### 6. 알림 설정 (향후 기능)

Langfuse는 알림 기능을 제공하지 않지만, 외부 모니터링 도구와 연동하여 알림을 설정할 수 있습니다:

- **Prometheus + Grafana**: 메트릭 수집 및 알림
- **Sentry**: 에러 추적 및 알림
- **Custom Script**: Langfuse API를 사용하여 주기적으로 에러 확인

## Langfuse API 사용

Langfuse는 REST API를 제공하여 프로그래밍 방식으로 데이터를 조회할 수 있습니다.

### API 키 사용

1. Settings > API Keys에서 Public Key와 Secret Key 확인
2. API 요청 시 헤더에 인증 정보 포함

### API 예시

Python으로 Langfuse API를 호출하는 예시:

```python
import requests

# Langfuse API 엔드포인트
LANGFUSE_HOST = "http://localhost:3000"
PUBLIC_KEY = "pk-lf-xxx"
SECRET_KEY = "sk-lf-xxx"

# Traces 조회
response = requests.get(
    f"{LANGFUSE_HOST}/api/public/traces",
    headers={
        "Authorization": f"Bearer {PUBLIC_KEY}:{SECRET_KEY}"
    },
    params={
        "limit": 10,
        "page": 1
    }
)

traces = response.json()
print(f"총 Trace 수: {len(traces['data'])}")

for trace in traces["data"]:
    print(f"- {trace['name']}: {trace['input']['source_text']}")
```

### API 문서

자세한 API 사용법은 [Langfuse API 문서](https://langfuse.com/docs/api)를 참고하세요.

## 데이터 보존 및 정리

Langfuse는 모든 Trace를 PostgreSQL에 저장하므로, 시간이 지나면 데이터베이스 크기가 증가합니다.

### 데이터 보존 정책

로컬 개발 환경에서는 데이터 보존 정책을 설정할 필요가 없지만, 프로덕션에서는 다음을 고려하세요:

- **보존 기간**: 최근 90일 데이터만 유지
- **아카이빙**: 오래된 데이터를 백업 후 삭제
- **데이터베이스 최적화**: 주기적으로 VACUUM 실행

### 데이터 정리

오래된 Trace를 삭제하려면:

1. PostgreSQL 접속:

   ```bash
   docker exec -it transbot-postgres psql -U transbot_user -d transbot
   ```

2. Langfuse 테이블 확인:

   ```sql
   \dt
   ```

3. 오래된 Trace 삭제 (예: 90일 이전 데이터):

   ```sql
   DELETE FROM traces WHERE created_at < NOW() - INTERVAL '90 days';
   ```

> **경고**: 데이터 삭제는 되돌릴 수 없습니다. 백업을 먼저 수행하세요.

## 다음 단계

- [Langfuse 설정 가이드](setup.md) - Langfuse 설치 및 API 키 생성
- [Langfuse 에러 핸들링 가이드](error-handling.md) - 에러 시나리오 및 문제 해결 방법
- [인프라 가이드](../../../infra/README.md) - Docker Compose 기반 인프라 사용법

## 관련 문서

- [Langfuse 공식 문서](https://langfuse.com/docs)
- [Langfuse Dashboard 가이드](https://langfuse.com/docs/analytics/overview)
- [Langfuse API 문서](https://langfuse.com/docs/api)

---

**작성일**: 2026-02-04
**최종 수정일**: 2026-02-04
**작성자**: TransBot Development Team
