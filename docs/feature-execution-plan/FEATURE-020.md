# FEATURE-020: 실시간 번역 결과 출력

## 개요

- **기능명**: 실시간 번역 결과 출력
- **상태**: 🔲 예정
- **분류**: 백엔드+프론트엔드
- **우선순위**: P2 (보통)
- **복잡도**: Standard (4-10h)
- **분석 수준**: 부분
- **진행률**: 0%
- **예상 시간**: 5시간
- **실제 소요**: - (완료 후 기록)
- **시작일**: -
- **완료일**: -

## 기능 설명

OpenAI API의 스트리밍 기능을 활용하여 번역 결과를 실시간으로 출력합니다. 사용자는 긴 번역 작업 시 번역 진행 상황을 실시간으로 확인할 수 있으며, 필요 시 중단 버튼으로 번역을 중단할 수 있습니다.

### 핵심 가치

- **체감 대기 시간 단축**: 전체 번역이 완료되기 전에 부분 결과를 먼저 확인
- **진행 상황 가시화**: 긴 텍스트 번역 시 진행 상태를 실시간으로 파악
- **사용자 제어권 향상**: 중단 버튼으로 불필요한 번역 작업 중지

## 배경 및 필요성

현재 TransBot은 동기 방식으로 번역을 수행하여 긴 텍스트 번역 시 사용자가 번역이 완료될 때까지 기다려야 합니다. 스트리밍 방식을 도입하면:

1. **UX 개선**: 첫 번째 문장부터 순차적으로 표시하여 체감 속도 향상
2. **피드백 제공**: 번역이 진행 중임을 명확히 표시
3. **비용 절감**: 중단 버튼으로 불필요한 토큰 소비 방지

## 요구사항

### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 |
| -- | -------- | -------- |
| FR-1 | OpenAI API 스트리밍 모드 지원 | 필수 |
| FR-2 | Azure OpenAI API 스트리밍 모드 지원 | 필수 |
| FR-3 | Streamlit UI에서 실시간 텍스트 출력 | 필수 |
| FR-4 | 스트리밍 중단 버튼 제공 | 필수 |
| FR-5 | 기존 동기 방식 `translate()` 메서드 유지 (하위 호환성) | 필수 |
| FR-6 | 모든 LLM 응답에 스트리밍 적용 (번역, 향후 사전 검색 등) | 선택 |

## 작업(Task) 분해

### Task 20.1: TranslationManager 스트리밍 메서드 추가 (백엔드)

**설명**: OpenAI API 스트리밍을 지원하는 `translate_stream()` 메서드를 추가합니다.

**세부 작업**:

1. `components/translation.py`의 `TranslationManager` 클래스에 `translate_stream()` 메서드 추가
2. OpenAI API 호출 시 `stream=True` 파라미터 추가
3. Generator 패턴으로 청크 단위 `yield` 구현
4. 에러 핸들링 추가 (스트리밍 중 오류 발생 시)
5. Docstring 작성 (파라미터, 반환값, 예외)

**예상 시간**: 1시간

**의존성**: 없음

**테스트 범위**:

- `translate_stream()` 메서드가 Generator를 반환하는지 확인
- 청크 단위로 텍스트가 반환되는지 확인
- 스트리밍 중 예외 발생 시 적절히 처리되는지 확인

**완료 조건**:

- [ ] `translate_stream()` 메서드 구현 완료
- [ ] Generator 패턴으로 청크 반환 확인
- [ ] 에러 핸들링 구현
- [ ] Docstring 작성 완료
- [ ] 타입 힌트 추가

**코드 예시**:

```python
def translate_stream(self, text: str, source: str, target: str):
    """텍스트를 스트리밍 방식으로 번역합니다.

    Args:
        text: 번역할 텍스트
        source: 원본 언어
        target: 대상 언어

    Yields:
        str: 번역된 텍스트 청크
    """
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following {source} text to {target}. IMPORTANT: Preserve all Markdown formatting."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=self.temperature,
        max_tokens=self.max_tokens,
        timeout=self.timeout,
        stream=True  # 스트리밍 활성화
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

### Task 20.2: AzureTranslationManager 스트리밍 지원 (백엔드)

**설명**: `AzureTranslationManager` 클래스에도 스트리밍 지원을 추가합니다.

**세부 작업**:

1. `AzureTranslationManager` 클래스에 `translate_stream()` 메서드 오버라이드
2. Azure deployment 방식으로 스트리밍 호출
3. Task 20.1과 동일한 Generator 패턴 적용
4. Docstring 작성

**예상 시간**: 0.5시간

**의존성**: Task 20.1

**테스트 범위**:

- Azure deployment로 스트리밍이 정상 동작하는지 확인
- OpenAI와 동일한 청크 반환 형식 확인

**완료 조건**:

- [ ] `translate_stream()` 메서드 오버라이드 완료
- [ ] Azure deployment 사용 확인
- [ ] Docstring 작성 완료

### Task 20.3: app.py 스트리밍 UI 구현 (프론트엔드)

**설명**: Streamlit의 `st.write_stream()`을 사용하여 번역 결과를 실시간으로 표시합니다.

**세부 작업**:

1. `app.py`의 번역 로직 수정 (Line 531-541)
2. `st.write_stream()` 사용하여 Generator 출력
3. 스트리밍 완료 후 `st.session_state.translation_result`에 전체 텍스트 저장
4. 기존 `st.spinner("번역 중...")` 블록 수정
5. 스트리밍 중 UI 상태 표시 (예: "번역 중..." 메시지)

**예상 시간**: 1시간

**의존성**: Task 20.1, Task 20.2

**테스트 범위**:

- 스트리밍 결과가 UI에 실시간으로 표시되는지 확인
- 스트리밍 완료 후 전체 텍스트가 저장되는지 확인
- 복사 버튼이 정상 동작하는지 확인

**완료 조건**:

- [ ] `st.write_stream()` 구현 완료
- [ ] 스트리밍 결과 실시간 표시 확인
- [ ] 전체 텍스트 저장 로직 구현
- [ ] 기존 UI 요소와 충돌 없음

**코드 예시**:

```python
# app.py 번역 로직 수정
with st.spinner("번역 중..."):
    try:
        # 스트리밍 결과를 저장할 변수
        full_result = ""

        # 스트리밍 출력
        result_placeholder = st.empty()
        for chunk in translation_manager.translate_stream(input_text, source_lang, target_lang):
            full_result += chunk
            result_placeholder.markdown(full_result)

        # 완료 후 세션 상태에 저장
        st.session_state.translation_result = {
            "text": full_result,
            "source": source_lang,
            "target": target_lang
        }
    except Exception as e:
        st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
```

### Task 20.4: 스트리밍 중단 버튼 추가 (프론트엔드)

**설명**: 사용자가 스트리밍 중 번역을 중단할 수 있는 버튼을 추가합니다.

**세부 작업**:

1. `st.session_state`에 중단 플래그 추가 (예: `stop_streaming`)
2. 스트리밍 중 "중단" 버튼 표시
3. 중단 버튼 클릭 시 `break`로 Generator 루프 종료
4. 중단 시 부분 결과를 `st.session_state`에 저장
5. 중단 메시지 표시 (예: "번역이 중단되었습니다")

**예상 시간**: 1시간

**의존성**: Task 20.3

**테스트 범위**:

- 중단 버튼이 스트리밍 중에만 표시되는지 확인
- 중단 버튼 클릭 시 즉시 중단되는지 확인
- 부분 결과가 저장되는지 확인

**완료 조건**:

- [ ] 중단 버튼 UI 추가
- [ ] 중단 플래그 구현
- [ ] 중단 시 부분 결과 저장
- [ ] 중단 메시지 표시

**코드 예시**:

```python
# 중단 버튼 추가
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 번역 결과")
with col2:
    if st.button("⏹️ 중단", key="stop_streaming"):
        st.session_state.stop_streaming = True

# 스트리밍 중 중단 체크
full_result = ""
result_placeholder = st.empty()

for chunk in translation_manager.translate_stream(input_text, source_lang, target_lang):
    if st.session_state.get("stop_streaming", False):
        st.warning("번역이 중단되었습니다.")
        break
    full_result += chunk
    result_placeholder.markdown(full_result)

# 중단 플래그 초기화
st.session_state.stop_streaming = False
```

### Task 20.5: 단위 테스트 작성 (테스트)

**설명**: 스트리밍 기능에 대한 단위 테스트를 작성합니다.

**세부 작업**:

1. `tests/test_translation.py`에 스트리밍 테스트 추가
2. Mock을 사용한 OpenAI 스트리밍 응답 시뮬레이션
3. Generator 반환값 검증
4. 청크 단위 데이터 검증
5. 에러 핸들링 테스트
6. Azure 스트리밍 테스트 추가

**예상 시간**: 1시간

**의존성**: Task 20.1, Task 20.2

**테스트 범위**:

- `translate_stream()` 메서드가 Generator를 반환하는지
- 청크가 순서대로 반환되는지
- 전체 결과가 올바른지
- 예외 발생 시 적절히 처리되는지

**완료 조건**:

- [ ] 최소 5개 테스트 케이스 작성
- [ ] 코드 커버리지 80% 이상 유지
- [ ] 모든 테스트 통과

**테스트 코드 예시**:

```python
def test_translate_stream_returns_generator(mock_client):
    """translate_stream()이 Generator를 반환하는지 테스트"""
    manager = TranslationManager(mock_client, model="gpt-4o")

    # Mock 응답 설정
    mock_client.chat.completions.create.return_value = [
        Mock(choices=[Mock(delta=Mock(content="Hello"))]),
        Mock(choices=[Mock(delta=Mock(content=" World"))])
    ]

    result = manager.translate_stream("안녕하세요", "Korean", "English")

    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')

def test_translate_stream_yields_chunks(mock_client):
    """translate_stream()이 청크를 순서대로 반환하는지 테스트"""
    manager = TranslationManager(mock_client, model="gpt-4o")

    mock_client.chat.completions.create.return_value = [
        Mock(choices=[Mock(delta=Mock(content="Hello"))]),
        Mock(choices=[Mock(delta=Mock(content=" World"))])
    ]

    chunks = list(manager.translate_stream("안녕하세요", "Korean", "English"))

    assert chunks == ["Hello", " World"]
    assert "".join(chunks) == "Hello World"
```

### Task 20.6: 문서 업데이트 (문서화)

**설명**: 스트리밍 기능 관련 문서를 업데이트합니다.

**세부 작업**:

1. README.md 업데이트 (스트리밍 기능 소개)
2. CLAUDE.md 업데이트 (개발자 가이드)
3. 스트리밍 사용 예시 추가
4. 최종 수정일시 업데이트

**예상 시간**: 0.5시간

**의존성**: 모든 Task 완료

**테스트 범위**:

- Markdownlint 규칙 준수
- 문서 내용 정확성

**완료 조건**:

- [ ] README.md 업데이트 완료
- [ ] CLAUDE.md 업데이트 완료
- [ ] Markdownlint 검사 통과

## 작업 흐름도

```text
Task 20.1: TranslationManager 스트리밍 메서드
    ↓
Task 20.2: AzureTranslationManager 스트리밍 지원
    ↓
Task 20.3: app.py 스트리밍 UI 구현
    ↓
Task 20.4: 스트리밍 중단 버튼 추가
    ↓
Task 20.5: 단위 테스트 작성
    ↓
Task 20.6: 문서 업데이트
```

## 완료 기준

- [ ] 번역 결과가 실시간으로 스트리밍 출력됨
- [ ] 중단 버튼이 정상 동작함
- [ ] 기존 동기 방식 `translate()` 메서드가 정상 동작함 (하위 호환성)
- [ ] OpenAI와 Azure OpenAI 모두 스트리밍 지원
- [ ] 모든 단위 테스트 통과 (커버리지 80% 이상)
- [ ] 문서 업데이트 완료

## 테스트 계획

### 수동 테스트 시나리오

| ID | 시나리오 | 예상 결과 |
| -- | -------- | --------- |
| MT-1 | 짧은 텍스트 (1문장) 번역 | 스트리밍으로 결과가 순차적으로 표시됨 |
| MT-2 | 긴 텍스트 (1000자 이상) 번역 | 첫 번째 문장부터 순차적으로 표시됨 |
| MT-3 | 스트리밍 중 중단 버튼 클릭 | 즉시 중단되고 부분 결과가 저장됨 |
| MT-4 | OpenAI Provider로 스트리밍 | 정상 동작 |
| MT-5 | Azure Provider로 스트리밍 | 정상 동작 |
| MT-6 | 스트리밍 완료 후 복사 버튼 | 전체 텍스트가 복사됨 |

### 자동 테스트

- **단위 테스트**: 최소 5개 테스트 케이스
  - `test_translate_stream_returns_generator`
  - `test_translate_stream_yields_chunks`
  - `test_translate_stream_full_result`
  - `test_translate_stream_error_handling`
  - `test_azure_translate_stream`

- **통합 테스트**: 향후 추가 고려

## 참고 자료

- [OpenAI API Streaming Documentation](https://platform.openai.com/docs/api-reference/streaming)
- [Streamlit write_stream Documentation](https://docs.streamlit.io/library/api-reference/write-magic/st.write_stream)
- [Python Generator Patterns](https://docs.python.org/3/howto/functional.html#generators)

---

**최종 수정일시**: 2026-02-03 20:14