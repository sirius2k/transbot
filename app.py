"""영어-한국어 번역기 Streamlit 애플리케이션"""
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils import strip_markdown
from components.language import LanguageDetector
from components.text import TextAnalyzer
from components.translation import TranslationManager

load_dotenv()


# ============================================================================
# Helper Functions (클립보드 복사 버튼)
# ============================================================================

def create_copy_button(text_to_copy: str, button_label: str = "📋 복사", button_key: str = "copy_btn") -> str:
    """클립보드 복사 버튼을 생성합니다.

    Args:
        text_to_copy: 복사할 텍스트
        button_label: 버튼 레이블
        button_key: 버튼 고유 키

    Returns:
        HTML 버튼 문자열
    """
    button_html = f"""
    <button onclick="copyToClipboard{button_key}()"
            style="background-color: #0066cc;
                   color: white;
                   border: none;
                   padding: 8px 16px;
                   border-radius: 4px;
                   cursor: pointer;
                   font-size: 14px;
                   margin-bottom: 10px;
                   margin-right: 8px;">
        {button_label}
    </button>
    <span id="feedback{button_key}" style="margin-left: 10px; color: green; display: none;">✅ 복사되었습니다!</span>
    <textarea id="copyText{button_key}" style="position: absolute; left: -9999px;">{text_to_copy}</textarea>
    <script>
    function copyToClipboard{button_key}() {{
        var copyText = document.getElementById("copyText{button_key}");
        copyText.select();
        document.execCommand("copy");

        var feedback = document.getElementById("feedback{button_key}");
        feedback.style.display = "inline";
        setTimeout(function() {{
            feedback.style.display = "none";
        }}, 2000);
    }}
    </script>
    """
    return button_html


def create_dual_copy_buttons(text_with_format: str, button_key_prefix: str = "dual") -> str:
    """포맷포함 복사와 텍스트만 복사 버튼을 함께 생성합니다.

    Args:
        text_with_format: 포맷이 포함된 텍스트
        button_key_prefix: 버튼 키 접두사

    Returns:
        HTML 버튼 문자열
    """
    text_only = strip_markdown(text_with_format)

    button_html = f"""
    <div style="margin-bottom: 10px;">
        <button onclick="copyWithFormat{button_key_prefix}()"
                style="background-color: #0066cc;
                       color: white;
                       border: none;
                       padding: 8px 16px;
                       border-radius: 4px;
                       cursor: pointer;
                       font-size: 14px;
                       margin-right: 8px;">
            📋 복사(포맷포함)
        </button>
        <button onclick="copyTextOnly{button_key_prefix}()"
                style="background-color: #28a745;
                       color: white;
                       border: none;
                       padding: 8px 16px;
                       border-radius: 4px;
                       cursor: pointer;
                       font-size: 14px;">
            📄 복사(텍스트만)
        </button>
        <span id="feedback{button_key_prefix}" style="margin-left: 10px; color: green; display: none;">✅ 복사되었습니다!</span>
    </div>
    <textarea id="copyTextWithFormat{button_key_prefix}" style="position: absolute; left: -9999px;">{text_with_format}</textarea>
    <textarea id="copyTextOnly{button_key_prefix}" style="position: absolute; left: -9999px;">{text_only}</textarea>
    <script>
    function copyWithFormat{button_key_prefix}() {{
        var copyText = document.getElementById("copyTextWithFormat{button_key_prefix}");
        copyText.select();
        document.execCommand("copy");

        var feedback = document.getElementById("feedback{button_key_prefix}");
        feedback.style.display = "inline";
        feedback.textContent = "✅ 복사되었습니다! (포맷포함)";
        setTimeout(function() {{
            feedback.style.display = "none";
        }}, 2000);
    }}

    function copyTextOnly{button_key_prefix}() {{
        var copyText = document.getElementById("copyTextOnly{button_key_prefix}");
        copyText.select();
        document.execCommand("copy");

        var feedback = document.getElementById("feedback{button_key_prefix}");
        feedback.style.display = "inline";
        feedback.textContent = "✅ 복사되었습니다! (텍스트만)";
        setTimeout(function() {{
            feedback.style.display = "none";
        }}, 2000);
    }}
    </script>
    """
    return button_html


def clear_inputs() -> None:
    """입력 텍스트와 번역 결과를 초기화하는 콜백 함수"""
    st.session_state.input_text = ""
    st.session_state.translation_result = None


# ============================================================================
# Configuration Functions (설정 및 초기화)
# ============================================================================

def initialize_page_config() -> None:
    """페이지 설정을 초기화합니다."""
    st.set_page_config(
        page_title="영어-한국어 번역기",
        page_icon="🌐",
        layout="centered"
    )


def initialize_session_state() -> None:
    """세션 상태를 초기화합니다."""
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'translation_result' not in st.session_state:
        st.session_state.translation_result = None


def setup_api_client() -> OpenAI:
    """OpenAI API 클라이언트를 설정하고 반환합니다.

    Returns:
        OpenAI 클라이언트 인스턴스
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input("OpenAI API Key", type="password")
        if not api_key:
            st.warning("OpenAI API 키를 입력해주세요.")
            st.stop()

    return OpenAI(api_key=api_key)


def initialize_components() -> tuple[LanguageDetector, TextAnalyzer]:
    """컴포넌트 인스턴스를 초기화합니다.

    Returns:
        (LanguageDetector, TextAnalyzer) 튜플
    """
    language_detector = LanguageDetector()
    text_analyzer = TextAnalyzer()
    return language_detector, text_analyzer


def setup_sidebar() -> tuple[str, dict[str, str]]:
    """사이드바를 설정하고 선택된 모델을 반환합니다.

    Returns:
        (선택된 모델명, 모델 옵션 딕셔너리) 튜플
    """
    st.sidebar.header("⚙️ 영어-한국어 번역기 설정")

    model_options = {
        "GPT-4o Mini (추천 - 가성비)": "gpt-4o-mini",
        "GPT-4o (최고 품질)": "gpt-4o",
        "GPT-4 Turbo": "gpt-4-turbo",
        "GPT-4": "gpt-4",
        "GPT-3.5 Turbo (빠름)": "gpt-3.5-turbo"
    }

    selected_model_name = st.sidebar.selectbox(
        "AI 모델 선택:",
        options=list(model_options.keys()),
        index=0  # 기본값: GPT-4o Mini
    )
    selected_model = model_options[selected_model_name]

    return selected_model, model_options


# ============================================================================
# UI Rendering Functions (UI 렌더링)
# ============================================================================

def show_title() -> None:
    """페이지 타이틀을 표시합니다."""
    st.title("🌐 영어-한국어 번역기")


def show_info_messages() -> None:
    """정보 메시지를 표시합니다."""
    st.info("🌐 **자동 번역**: 입력하신 언어를 자동으로 감지하여 번역합니다.")
    st.info("💡 **Markdown 지원**: **볼드**, *이탤릭*, `코드`, [링크](URL), 리스트(- 또는 1.), > 인용문, 표 등 사용 가능")


def render_input_area() -> st.delta_generator.DeltaGenerator:
    """입력 영역을 렌더링하고 통계 placeholder를 반환합니다.

    Returns:
        통계를 표시할 placeholder
    """
    # 원문 입력 영역 - 타이틀과 통계를 좌우로 나누기
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**원문 (Markdown 지원)**")
    with col2:
        stats_placeholder = st.empty()

    # 입력 텍스트 영역
    st.text_area(
        "원문",
        placeholder="번역할 텍스트를 입력하세요... (한국어/English 자동 감지)",
        height=200,
        label_visibility="collapsed",
        key="input_text"
    )

    return stats_placeholder


def render_action_buttons(
    input_text: str,
    source_lang: str,
    target_lang: str,
    translation_manager: TranslationManager
) -> None:
    """번역하기와 지우기 버튼을 렌더링합니다.

    Args:
        input_text: 입력 텍스트
        source_lang: 원본 언어
        target_lang: 대상 언어
        translation_manager: 번역 관리자 인스턴스
    """
    col_btn1, col_btn2 = st.columns([3, 1])

    with col_btn1:
        if st.button("번역하기", type="primary", use_container_width=True):
            handle_translation(input_text, source_lang, target_lang, translation_manager)

    with col_btn2:
        st.button("🗑️ 지우기", use_container_width=True, on_click=clear_inputs)


def render_translation_result() -> None:
    """번역 결과를 렌더링합니다."""
    if st.session_state.translation_result:
        result = st.session_state.translation_result["text"]
        source_lang = st.session_state.translation_result["source"]
        target_lang = st.session_state.translation_result["target"]

        # 번역 방향 표시
        direction_text = f"{source_lang} → {target_lang}"
        st.subheader(f"번역 결과 ({direction_text})")

        # 탭으로 번역문과 Markdown 원본 제공
        tab1, tab2 = st.tabs(["📄 번역문", "📝 Markdown 원본"])

        with tab1:
            # 번역문 복사 버튼 (포맷포함 / 텍스트만)
            st.components.v1.html(
                create_dual_copy_buttons(result, "translation"),
                height=60
            )
            st.markdown(result)

        with tab2:
            # Markdown 원본 복사 버튼
            st.components.v1.html(
                create_copy_button(result, "📋 Markdown 복사", "markdown"),
                height=50
            )
            st.code(result, language="markdown", line_numbers=False)


# ============================================================================
# Logic Functions (비즈니스 로직)
# ============================================================================

def update_statistics(
    input_text: str,
    stats_placeholder: st.delta_generator.DeltaGenerator,
    language_detector: LanguageDetector,
    text_analyzer: TextAnalyzer,
    selected_model: str
) -> tuple[str, str, str]:
    """입력 텍스트의 통계를 업데이트하고 언어를 감지합니다.

    Args:
        input_text: 입력 텍스트
        stats_placeholder: 통계를 표시할 placeholder
        language_detector: 언어 감지기 인스턴스
        text_analyzer: 텍스트 분석기 인스턴스
        selected_model: 선택된 모델명

    Returns:
        (source_lang, target_lang, direction_arrow) 튜플
    """
    if input_text:
        # 언어 감지 및 번역 방향 결정
        source_lang, target_lang, direction_arrow = language_detector.get_translation_direction(input_text)

        # 통계 표시 HTML 생성
        text_analyzer.model = selected_model
        stats_html = text_analyzer.format_statistics_display(input_text, direction_arrow)
        stats_placeholder.markdown(stats_html, unsafe_allow_html=True)
    else:
        source_lang = "unknown"
        target_lang = "unknown"
        stats_placeholder.markdown(
            "<div style='text-align: right; color: #888;'>0자 / 0 토큰</div>",
            unsafe_allow_html=True
        )

    return source_lang, target_lang, direction_arrow


def handle_translation(
    input_text: str,
    source_lang: str,
    target_lang: str,
    translation_manager: TranslationManager
) -> None:
    """번역을 처리합니다.

    Args:
        input_text: 입력 텍스트
        source_lang: 원본 언어
        target_lang: 대상 언어
        translation_manager: 번역 관리자 인스턴스
    """
    if not input_text.strip():
        st.warning("번역할 텍스트를 입력해주세요.")
        return

    if source_lang == "unknown" or target_lang == "unknown":
        st.error("언어를 감지할 수 없습니다. 한국어 또는 영어 텍스트를 입력해주세요.")
        return

    with st.spinner("번역 중..."):
        try:
            result = translation_manager.translate(input_text, source_lang, target_lang)
            st.session_state.translation_result = {
                "text": result,
                "source": source_lang,
                "target": target_lang
            }
        except Exception as e:
            st.error(f"번역 중 오류가 발생했습니다: {str(e)}")


# ============================================================================
# Main Function
# ============================================================================

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
        input_text,
        stats_placeholder,
        language_detector,
        text_analyzer,
        selected_model
    )

    # 8. 액션 버튼 렌더링
    render_action_buttons(input_text, source_lang, target_lang, translation_manager)

    # 9. 번역 결과 표시
    render_translation_result()


if __name__ == "__main__":
    main()
