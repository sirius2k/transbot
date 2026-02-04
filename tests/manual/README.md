# Manual Tests

이 디렉토리는 자동화할 수 없는 테스트나 실제 환경에서 검증이 필요한 테스트를 포함합니다.

## test_error_scenarios.py

Langfuse 에러 핸들링을 검증하는 테스트 스크립트입니다.

### 실행 방법

```bash
# 프로젝트 루트에서 실행
python3 tests/manual/test_error_scenarios.py
```

### 테스트 시나리오

1. **환경 변수 미설정**
   - Langfuse 환경 변수가 설정되지 않은 경우
   - `Config.langfuse_enabled`가 False여야 함
   - `LangfuseObserver._client`가 None이어야 함
   - 번역 기능은 정상 동작해야 함

2. **잘못된 API 키**
   - 잘못된 Langfuse API 키로 초기화 시
   - `LangfuseObserver._init_failed`가 True여야 함
   - 에러 메시지가 출력되어야 함
   - 번역 기능은 정상 동작해야 함

3. **Langfuse 서버 다운**
   - Langfuse 컨테이너가 중지된 경우
   - 연결 에러가 적절히 처리되어야 함
   - 번역 기능은 정상 동작해야 함

4. **네트워크 타임아웃**
   - 존재하지 않는 URL로 연결 시
   - 타임아웃 에러가 적절히 처리되어야 함
   - 번역 기능은 정상 동작해야 함

### 주의사항

- 테스트 실행 시 `.env` 파일이 자동으로 백업 및 복원됩니다.
- 시나리오 3은 Langfuse Docker 컨테이너를 중지/재시작합니다.
- 모든 테스트는 번역 기능이 정상 동작하는지 확인합니다.
- 에러는 콘솔에만 출력되고 UI에는 표시되지 않습니다.

### 테스트 결과

테스트 결과는 터미널에 색상과 함께 출력됩니다.

- ✓ (녹색): 테스트 통과
- ✗ (빨간색): 테스트 실패
- ⚠ (노란색): 경고 메시지
- ℹ (청록색): 정보 메시지
