# MINOR-002: 콘솔에서의 로깅 간소화

## 개요

- **기능명**: 콘솔에서의 로깅 간소화
- **상태**: ✅ 완료
- **분류**: 백엔드
- **우선순위**: P2 (보통)
- **복잡도**: Quick Win (0.17h)
- **분석 수준**: 없음
- **진행률**: 100%
- **예상 시간**: 0.17시간 (10분)
- **실제 소요**: 0.17시간
- **시작일**: 2026-01-25
- **완료일**: 2026-01-25

## 기능 설명

콘솔과 파일에 서로 다른 포맷터를 적용하여 개발 경험을 개선합니다. 콘솔은 사람이 읽기 쉬운 형식으로, 파일은 구조화된 JSON 형식으로 유지하여 각각의 목적에 맞게 최적화합니다.

### 기대 효과

- 콘솔 출력이 간결하고 읽기 쉬워짐
- 파일 로그는 JSON 형식 유지로 파싱 및 분석 용이
- 개발자 경험 개선 (DX)

## 작업 내용

1. **콘솔 핸들러에 간단한 포맷터 적용**
   - 시간, 레벨, 메시지만 표시
   - 불필요한 메타데이터 제거
   - 색상 코딩 적용 (선택적)

2. **파일 핸들러는 JSONFormatter 유지**
   - 기존 JSONFormatter 그대로 유지
   - 구조화된 로그로 분석 도구 활용 가능

3. **logger.py 수정**
   - `setup_logging()` 함수에서 핸들러별 포맷터 분리
   - 기존 로그 레벨 및 설정 유지

**예상 파일**:

- `logger.py` - 포맷터 분리 로직 추가

## 완료 기준

- [x] 콘솔 출력이 간결한 형식으로 표시됨
- [x] 파일 로그는 JSON 형식 유지됨
- [x] 로그 레벨 및 기능에 영향 없음
- [x] 기존 로그 분석 도구 정상 동작

## 구현 결과

### 구현 내용

`logger.py`의 `setup_logging()` 함수를 수정하여 핸들러별 포맷터를 분리했습니다:

1. **콘솔 핸들러**: `logging.Formatter` 사용
   - 형식: `%(asctime)s - %(levelname)s - %(message)s`
   - 사람이 읽기 쉬운 간결한 출력

2. **파일 핸들러**: `JSONFormatter` 유지
   - 구조화된 JSON 로그
   - 분석 도구 및 모니터링 시스템 활용 가능

### 코드 예시

```python
def setup_logging():
    # 콘솔 핸들러: 간단한 포맷
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # 파일 핸들러: JSON 포맷
    file_handler = RotatingFileHandler(...)
    file_handler.setFormatter(JSONFormatter())
```

### 테스트 결과

- ✅ 콘솔 출력이 읽기 쉬워짐
- ✅ 파일 로그는 JSON 형식 유지
- ✅ 로그 분석 스크립트 정상 동작
- ✅ Langfuse 연동 영향 없음

## 참고 사항

- 개발 환경과 프로덕션 환경 모두 개선
- 기존 로그 파싱 로직 변경 불필요
- 최소한의 수정으로 최대 효과

---

**최종 수정일**: 2026-02-09
