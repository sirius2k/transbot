"""LLM 관찰성 모듈

Langfuse를 통한 LLM 사용 추적 및 모니터링 기능을 제공합니다.
"""

from typing import Optional

from langfuse import Langfuse

from config import Config


class LangfuseObserver:
    """Langfuse를 통한 LLM 관찰성 추적 클래스

    LLM API 호출을 Langfuse에 추적하여 비용 분석, 품질 모니터링,
    프롬프트 최적화를 위한 데이터를 수집합니다.

    Langfuse가 비활성화되어 있거나 초기화에 실패한 경우,
    모든 메서드는 no-op으로 동작하여 애플리케이션에 영향을 주지 않습니다.

    Attributes:
        config: Config 객체
        _client: Langfuse 클라이언트 인스턴스 (None일 수 있음)
        _init_failed: 초기화 실패 여부
    """

    def __init__(self, config: Config):
        """LangfuseObserver 초기화

        Args:
            config: 설정 객체
        """
        self.config = config
        self._client: Optional[Langfuse] = None
        self._init_failed = False

        if not self.config.langfuse_enabled:
            return

        try:
            self._client = Langfuse(
                public_key=config.LANGFUSE_PUBLIC_KEY,
                secret_key=config.LANGFUSE_SECRET_KEY,
                host=config.LANGFUSE_HOST,
                timeout=5  # 5초 타임아웃
            )
        except Exception as e:
            self._init_failed = True
            print(f"⚠️ Langfuse 초기화 실패 (추적 비활성화): {e}")
            self._client = None

    def track_translation(
        self,
        source_text: str,
        target_text: str,
        source_lang: str,
        target_lang: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        session_id: str,
        error: Optional[str] = None
    ) -> None:
        """번역 요청 추적

        번역 요청의 입력/출력, 토큰 사용량, 응답 시간 등을
        Langfuse에 전송합니다.

        Args:
            source_text: 원본 텍스트
            target_text: 번역된 텍스트
            source_lang: 원본 언어 코드 (예: 'en', 'ko')
            target_lang: 대상 언어 코드 (예: 'en', 'ko')
            model: 사용된 AI 모델 (예: 'gpt-4o-mini')
            input_tokens: 입력 토큰 수
            output_tokens: 출력 토큰 수
            latency_ms: 응답 시간 (밀리초)
            session_id: 세션 ID (사용자 세션별 그룹핑용)
            error: 에러 메시지 (에러 발생 시)
        """
        if not self._client or self._init_failed:
            return

        try:
            # Langfuse v2 API: trace 객체 생성 후 generation 추가
            trace = self._client.trace(
                name="translation",
                session_id=session_id,
                metadata={
                    "direction": f"{source_lang}→{target_lang}",
                    "latency_ms": latency_ms,
                },
            )

            # LLM 호출 정보를 generation으로 추가
            trace.generation(
                name="translation_llm_call",
                model=model,
                input={
                    "source_text": source_text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                },
                output={"target_text": target_text},
                usage={
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens,
                },
                level="ERROR" if error else "DEFAULT",
                status_message=error,
            )
        except TimeoutError:
            print("⚠️ Langfuse 전송 타임아웃 (추적 건너뜀)")
        except Exception as e:
            print(f"⚠️ Langfuse 추적 실패: {type(e).__name__}: {e}")

    def flush(self) -> None:
        """Pending 데이터를 Langfuse로 전송

        메모리에 보류 중인 추적 데이터를 Langfuse 서버로 전송합니다.
        애플리케이션 종료 전에 호출하여 데이터 손실을 방지할 수 있습니다.
        """
        if self._client:
            try:
                self._client.flush()
            except Exception as e:
                print(f"⚠️ Langfuse flush 실패: {e}")
