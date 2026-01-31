# app.py 구조 가이드

app.py는 **함수 기반으로 구조화**되어 있으며, 각 함수는 명확한 책임을 가지고 있습니다.

## 전체 구조 개요

- **총 라인 수**: 427줄
- **총 함수 수**: 15개 함수 + 1개 main() 진입점
- **섹션 구분**: 5개 섹션으로 명확히 분리
- **설계 철학**: 관심사 분리(Separation of Concerns), 단일 책임 원칙(SRP)

## 섹션별 함수 목록

### 1. Helper Functions (3개) - 클립보드 복사 버튼

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `create_copy_button()` | 단일 복사 버튼 HTML 생성 | text_to_copy, button_label, button_key | str |
| `create_dual_copy_buttons()` | 듀얼 복사 버튼 HTML 생성 (포맷포함/텍스트만) | text_with_format, button_key_prefix | str |
| `clear_inputs()` | 세션 상태 초기화 콜백 | 없음 | None |

### 2. Configuration Functions (5개) - 설정 및 초기화

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `initialize_page_config()` | 페이지 설정 초기화 | 없음 | None |
| `initialize_session_state()` | 세션 상태 초기화 | 없음 | None |
| `setup_api_client()` | OpenAI API 클라이언트 설정 | 없음 | OpenAI |
| `initialize_components()` | 컴포넌트 인스턴스 초기화 | 없음 | tuple[LanguageDetector, TextAnalyzer] |
| `setup_sidebar()` | 사이드바 설정 및 모델 선택 | 없음 | tuple[str, dict[str, str]] |

### 3. UI Rendering Functions (5개) - UI 렌더링

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `show_title()` | 페이지 타이틀 표시 | 없음 | None |
| `show_info_messages()` | 정보 메시지 표시 | 없음 | None |
| `render_input_area()` | 입력 영역 렌더링 | 없음 | st.delta_generator.DeltaGenerator |
| `render_action_buttons()` | 액션 버튼 렌더링 (번역하기/지우기) | input_text, source_lang, target_lang, translation_manager | None |
| `render_translation_result()` | 번역 결과 렌더링 | 없음 | None |

### 4. Logic Functions (2개) - 비즈니스 로직

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `update_statistics()` | 통계 업데이트 및 언어 감지 | input_text, stats_placeholder, language_detector, text_analyzer, selected_model | tuple[str, str, str] |
| `handle_translation()` | 번역 처리 로직 | input_text, source_lang, target_lang, translation_manager | None |

### 5. Main Function (1개) - 애플리케이션 진입점

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `main()` | 메인 애플리케이션 흐름 조율 (9단계) | 없음 | None |

## main() 함수 실행 흐름 (9단계)

```python
def main() -> None:
    """메인 애플리케이션 함수"""
    # 1. 페이지 설정 및 초기화
    initialize_page_config()
    initialize_session_state()

    # 2. 타이틀 표시
    show_title()

    # 3. API 클라이언트 및 컴포넌트 초기화
    client = setup_api_client()
    language_detector, text_analyzer = initialize_components()

    # 4. 사이드바 설정 및 번역 관리자 초기화
    selected_model, _ = setup_sidebar()
    translation_manager = TranslationManager(client, model=selected_model)

    # 5. 정보 메시지 표시
    show_info_messages()

    # 6. 입력 영역 렌더링
    stats_placeholder = render_input_area()

    # 7. 통계 업데이트 및 언어 감지
    input_text = st.session_state.input_text
    source_lang, target_lang, _ = update_statistics(
        input_text, stats_placeholder, language_detector, text_analyzer, selected_model
    )

    # 8. 액션 버튼 렌더링
    render_action_buttons(input_text, source_lang, target_lang, translation_manager)

    # 9. 번역 결과 표시
    render_translation_result()
```

## 함수 기반 설계의 장점

### 코드 품질 지표

| 지표 | 변경 전 (인라인 코드) | 변경 후 (함수 기반) | 개선률 |
| ---- | ------------------- | ------------------ | ------ |
| 함수 개수 | 3개 | 15개 | +400% |
| 최상위 레벨 코드 | 200줄 | 0줄 | -100% |
| 최대 함수 길이 | 94줄 | 38줄 | -60% |
| 테스트 가능 함수 | 2개 | 10개 | +400% |
| Docstring 커버리지 | 67% | 100% | +33% |
| 타입 힌트 적용 | 부분적 | 전체 | +100% |

### 개선 효과

1. **가독성**: 명확한 섹션 구분으로 코드 이해 용이
2. **유지보수성**: 함수별 독립적 수정 가능
3. **테스트 용이성**: 순수 함수로 단위 테스트 작성 가능
4. **재사용성**: 설정/렌더링/로직 함수 분리
5. **확장성**: 새로운 기능 추가 시 기존 함수에 영향 최소화

## 함수 작성 규칙

1. **명확한 책임**: 각 함수는 하나의 명확한 책임만 가짐
2. **타입 힌트 필수**: 모든 매개변수와 반환 타입에 타입 힌트 명시
3. **Docstring 작성**: 함수 목적, 매개변수, 반환값 설명
4. **섹션 주석**: 각 섹션은 주석으로 명확히 구분
5. **매개변수 명시**: 전역 변수 대신 명시적 매개변수 사용

## 향후 확장 계획

### Phase 2: UI 컴포넌트 클래스화

현재 `create_copy_button()`, `create_dual_copy_buttons()` 함수를 클래스로 전환 예정:

```python
# components/ui/clipboard.py (예정)
class ClipboardButton:
    """클립보드 복사 버튼 컴포넌트"""

    def __init__(self, style_config: dict = None):
        self.style_config = style_config or self._default_style()

    def create_single_button(self, text: str, label: str, key: str) -> str:
        """단일 복사 버튼 생성"""
        pass

    def create_dual_buttons(self, text: str, key_prefix: str) -> str:
        """듀얼 복사 버튼 생성"""
        pass
```

## 파일 수정 시 주의사항

- **함수 기반 구조 유지**: 새로운 기능은 적절한 섹션에 함수로 추가
- **섹션 구분 준수**: Helper / Configuration / UI Rendering / Logic / Main 섹션 구분
- **main() 흐름 명확성**: main() 함수는 9단계 흐름을 유지하며 간결하게 작성
- Streamlit 컴포넌트 구조 유지
- 에러 핸들링 반드시 포함
- 사용자 경험을 최우선으로 고려
- 비즈니스 로직은 components 모듈로 분리
- **타입 힌트 및 Docstring 필수**

---

마지막 업데이트: 2026-01-31
