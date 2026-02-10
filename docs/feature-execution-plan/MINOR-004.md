# MINOR-004: Langfuse Prompt 표시 개선

## 개요

- **기능명**: Langfuse Prompt 표시 개선
- **상태**: ✅ 완료
- **분류**: 백엔드
- **우선순위**: P2 (보통)
- **복잡도**: Quick Win (0.5h)
- **분석 수준**: 없음
- **진행률**: 100%
- **예상 시간**: 0.5시간 (30분)
- **실제 소요**: 0.5시간
- **시작일**: 2026-02-06
- **완료일**: 2026-02-06

## 기능 설명

Langfuse Generation에 Prompt 섹션을 추가하여 LLM 호출 시 전송된 시스템 메시지와 사용자 메시지를 Langfuse 대시보드에서 확인할 수 있도록 개선합니다. 프롬프트 디버깅 및 최적화에 필수적인 정보를 제공합니다.

### 기대 효과

- Langfuse에서 전체 프롬프트 확인 가능
- 프롬프트 버전 비교 및 A/B 테스트 용이
- 디버깅 시간 단축
- 프롬프트 품질 개선을 위한 인사이트 확보

## 작업 내용

1. **Langfuse Generation API 확인**
   - `prompt` 파라미터 지원 여부 확인
   - 메시지 구조 (system, user) 지원 여부 확인

2. **LangfuseObserver 수정**
   - `end_generation()` 메서드에서 프롬프트 데이터 추가
   - 시스템 메시지와 사용자 메시지 구분하여 전송
   - 기존 메타데이터와 충돌 없도록 구현

3. **테스트 및 검증**
   - Langfuse 대시보드에서 Prompt 섹션 표시 확인
   - 메시지 내용이 정확하게 표시되는지 검증

**예상 파일**:

- `components/observability.py` - LangfuseObserver 클래스 수정

## 완료 기준

- [x] Langfuse Generation에 Prompt 섹션 추가됨
- [x] 시스템 메시지가 정확하게 표시됨
- [x] 사용자 메시지가 정확하게 표시됨
- [x] 기존 메타데이터 기능에 영향 없음
- [x] Langfuse 대시보드에서 정상 조회됨

## 구현 결과

### 구현 내용

`components/observability.py`의 `LangfuseObserver.end_generation()` 메서드를 수정했습니다:

1. **Prompt 데이터 구조**:
   ```python
   prompt = [
       {"role": "system", "content": system_message},
       {"role": "user", "content": user_message}
   ]
   ```

2. **Langfuse API 호출**:
   - `generation.update(prompt=prompt)` 사용
   - OpenAI Chat Completions 형식과 동일한 구조

### 코드 예시

```python
def end_generation(self, generation_id: str, response: str,
                   system_message: str, user_message: str):
    """Generation 종료 및 프롬프트 기록"""
    try:
        generation = self.langfuse.get_generation(generation_id)

        # Prompt 추가
        prompt = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        generation.update(
            output=response,
            prompt=prompt,
            end_time=datetime.now()
        )
    except Exception as e:
        # Graceful degradation
        logger.error(f"Langfuse generation 업데이트 실패: {e}")
```

### 테스트 결과

- ✅ Langfuse 대시보드에서 Prompt 섹션 확인됨
- ✅ System 메시지와 User 메시지가 명확히 구분됨
- ✅ 프롬프트 비교 기능 정상 동작
- ✅ 기존 메타데이터와 충돌 없음

### Langfuse 대시보드 스크린샷 예시

```
Generation Details
├── Prompt
│   ├── System: "You are a professional translator..."
│   └── User: "Translate the following text..."
├── Output: "번역된 텍스트..."
├── Metadata: {...}
└── Timing: 2.3s
```

## 참고 사항

- Langfuse v2 API 사용
- OpenAI Chat Completions 형식과 호환
- 프롬프트 템플릿 관리 기능 향후 추가 가능
- 프롬프트 버전 관리 및 A/B 테스트 기반 마련

## 관련 문서

- [Langfuse Prompt Management](https://langfuse.com/docs/prompts)
- [FEATURE-016: Langfuse 연동](../feature-execution-plan/FEATURE-016.md)

---

**최종 수정일**: 2026-02-09
