"""영어-한국어 번역기 Streamlit 애플리케이션"""
import streamlit as st
import os
import uuid
from typing import Any, Literal
from dotenv import load_dotenv
from utils import strip_markdown
from components.language import LanguageDetector
from components.text import TextAnalyzer
from components.translation import TranslationManager
from config import Config
from components.observability import configure_langfuse
from logger import setup_logging, get_logger

load_dotenv()

# 설정 로드
config = Config.load()

# 로깅 시스템 초기화
setup_logging(config)
logger = get_logger("transbot.app")

# Langfuse 관찰성 초기화
configure_langfuse(config)


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
    st.session_state.input_text = ""
    st.session_state.translation_result = None
    # FEATURE-023: 스타일 옵션 관련 상태 초기화
    st.session_state.translation_completed = False
    st.session_state.source_language = ""
    st.session_state.target_language = ""
    st.session_state.selected_styles = []
    st.session_state.multi_style_results = None


def format_translation_result(text: str) -> str:
    """번역 결과의 포맷을 보존합니다.

    Markdown에서 줄바꿈을 올바르게 표시하기 위해
    각 줄 끝에 두 개의 공백을 추가합니다.

    Args:
        text: 원본 텍스트

    Returns:
        포맷이 보존된 텍스트
    """
    # 각 줄 끝에 두 공백 추가 (Markdown 줄바꿈 규칙)
    lines = text.split('\n')
    formatted_lines = [line + '  ' if line.strip() else line for line in lines]
    return '\n'.join(formatted_lines)


# ============================================================================
# Configuration Functions (설정 및 초기화)
# ============================================================================

def initialize_page_config() -> None:
    """페이지 설정을 초기화합니다.

    Config에서 APP_TITLE, APP_ICON, APP_LAYOUT을 로드하여 적용합니다.
    """
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.APP_LAYOUT
    )


def initialize_session_state() -> None:
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'translation_result' not in st.session_state:
        st.session_state.translation_result = None
    # FEATURE-023: 스타일 옵션 관련 상태
    if 'translation_completed' not in st.session_state:
        st.session_state.translation_completed = False
    if 'source_language' not in st.session_state:
        st.session_state.source_language = ""
    if 'target_language' not in st.session_state:
        st.session_state.target_language = ""
    if 'selected_styles' not in st.session_state:
        st.session_state.selected_styles = []
    if 'multi_style_results' not in st.session_state:
        st.session_state.multi_style_results = None


def setup_api_client() -> tuple[Any, Literal["openai", "azure"]]:
    """OpenAI/Azure API 클라이언트를 설정하고 반환합니다.

    Returns:
        (client, provider) 튜플
    """
    # 전역 config 사용
    provider = config.AI_PROVIDER

    logger.info("API 클라이언트 초기화 시작", extra={"provider": provider})

    if provider == "azure":
        # Azure 필수 파라미터 검증
        if not config.AZURE_OPENAI_API_KEY:
            st.error("⚠️ AZURE_OPENAI_API_KEY가 설정되지 않았습니다.")
            st.stop()
        if not config.AZURE_OPENAI_ENDPOINT:
            st.error("⚠️ AZURE_OPENAI_ENDPOINT가 설정되지 않았습니다.")
            st.stop()

        # AzureOpenAI 클라이언트 생성
        from openai import AzureOpenAI

        azure_client: Any = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_version=config.AZURE_OPENAI_API_VERSION,
            timeout=config.OPENAI_API_TIMEOUT,
            max_retries=config.OPENAI_MAX_RETRIES
        )

        # Azure deployment 목록 로드
        from components.translation import AzureTranslationManager
        AzureTranslationManager.load_deployments(config)

        logger.info("Azure API 클라이언트 생성 성공", extra={
            "provider": "azure",
            "api_version": config.AZURE_OPENAI_API_VERSION
        })

        return azure_client, "azure"
    else:
        # OpenAI 클라이언트 생성
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = st.sidebar.text_input("OpenAI API Key", type="password")
            if not api_key:
                st.warning("OpenAI API 키를 입력해주세요.")
                st.stop()

        from openai import OpenAI

        openai_client: Any = OpenAI(
            api_key=api_key,
            timeout=config.OPENAI_API_TIMEOUT,
            max_retries=config.OPENAI_MAX_RETRIES
        )

        logger.info("OpenAI API 클라이언트 생성 성공", extra={"provider": "openai"})

        return openai_client, "openai"


def initialize_components() -> tuple[LanguageDetector, TextAnalyzer]:
    """컴포넌트 인스턴스를 초기화합니다.

    Returns:
        (LanguageDetector, TextAnalyzer) 튜플
    """
    language_detector = LanguageDetector()
    text_analyzer = TextAnalyzer()
    return language_detector, text_analyzer


def setup_sidebar(provider: Literal["openai", "azure"]) -> tuple[str, dict[str, str]]:
    """사이드바를 설정하고 선택된 모델/deployment를 반환합니다.

    Provider에 따라 모델 목록 또는 deployment 목록을 표시합니다.

    Args:
        provider: "openai" 또는 "azure"

    Returns:
        (선택된 모델/deployment명, 옵션 딕셔너리) 튜플
    """
    st.sidebar.header("⚙️ 설정")
    st.sidebar.markdown("---")

    # 모델 선택을 먼저 표시
    if provider == "azure":
        # Azure: Deployment 목록 표시
        from components.translation import AzureTranslationManager

        deployments = AzureTranslationManager.SUPPORTED_DEPLOYMENTS

        if not deployments:
            st.sidebar.error(
                "⚠️ **Azure Deployment 미설정**\n\n"
                "`.env` 파일에 `AZURE_DEPLOYMENTS` 설정을 추가해주세요.\n\n"
                "예시:\n"
                "```\n"
                "AZURE_DEPLOYMENTS=gpt-4o:my-gpt4o,gpt-4o-mini:my-mini\n"
                "```"
            )
            st.stop()

        # Deployment 옵션 생성 (모델명을 표시명으로 사용)
        deployment_options = {
            f"{model} (Azure)": deployment
            for model, deployment in deployments.items()
        }

        # Config에서 기본 모델 가져오기
        default_model = config.DEFAULT_MODEL

        # 기본 모델에 해당하는 인덱스 찾기
        default_index = 0
        for idx, model_name in enumerate(deployments.keys()):
            if model_name == default_model:
                default_index = idx
                break

        selected_deployment_name: str = st.sidebar.selectbox(
            "Azure Deployment 선택:",
            options=list(deployment_options.keys()),
            index=default_index
        )  # type: ignore
        selected_model_or_deployment = deployment_options[selected_deployment_name]
        options = deployment_options

    else:
        # OpenAI: 환경 변수 기반 모델 목록 표시
        model_options = config.get_available_openai_models()

        # 모델이 하나도 없는 경우 에러 표시
        if not model_options:
            st.sidebar.error(
                "⚠️ **사용 가능한 모델 없음**\n\n"
                "환경 변수 `OPENAI_MODELS`에 유효한 모델을 설정해주세요.\n\n"
                "지원 모델: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo"
            )
            st.stop()

        # Config에서 기본 모델 가져오기
        default_model = config.DEFAULT_MODEL

        # 기본 모델에 해당하는 인덱스 찾기
        default_index = 0
        for idx, (_, model_id) in enumerate(model_options.items()):
            if model_id == default_model:
                default_index = idx
                break

        selected_model_name: str = st.sidebar.selectbox(
            "AI 모델 선택:",
            options=list(model_options.keys()),
            index=default_index
        )  # type: ignore
        selected_model_or_deployment = model_options[selected_model_name]
        options = model_options

    # 포맷 유지 옵션
    st.sidebar.checkbox(
        "📝 포맷 유지",
        value=True,
        key="preserve_format",
        help="번역 결과의 줄바꿈과 들여쓰기를 보존합니다."
    )

    st.sidebar.markdown("---")

    # FEATURE-024: 번역 스타일 옵션 개선
    st.sidebar.markdown("#### 🎨 번역 스타일 옵션")
    st.sidebar.markdown("**번역 스타일 선택** (다중 선택 가능)")

    # StyleTranslator 상수 import
    from components.style_translator import StyleTranslator

    # 스타일 선택 체크박스 (기본값: 직역만 선택)
    # 직역을 최상단에 배치
    style_literal = st.sidebar.checkbox(
        StyleTranslator.STYLE_LABELS[StyleTranslator.STYLE_LITERAL],
        value=True,  # 기본 선택
        key="style_literal"
    )
    style_conversational = st.sidebar.checkbox(
        StyleTranslator.STYLE_LABELS[StyleTranslator.STYLE_CONVERSATIONAL],
        value=False,
        key="style_conversational"
    )
    style_business = st.sidebar.checkbox(
        StyleTranslator.STYLE_LABELS[StyleTranslator.STYLE_BUSINESS],
        value=False,
        key="style_business"
    )
    style_formal = st.sidebar.checkbox(
        StyleTranslator.STYLE_LABELS[StyleTranslator.STYLE_FORMAL],
        value=False,
        key="style_formal"
    )
    style_concise = st.sidebar.checkbox(
        StyleTranslator.STYLE_LABELS[StyleTranslator.STYLE_CONCISE],
        value=False,
        key="style_concise"
    )

    # 커스텀 스타일 체크박스
    style_custom = st.sidebar.checkbox(
        "✍️ 커스텀 스타일",
        value=False,
        key="style_custom_checkbox",
        help="직접 번역 스타일을 지정할 수 있습니다."
    )

    # 커스텀 스타일이 선택된 경우에만 입력 박스 표시
    if style_custom:
        custom_instruction = st.sidebar.text_area(
            "커스텀 스타일 지침",
            value="",
            key="custom_style_instruction",
            height=100,
            placeholder="예: 유머러스한 톤으로 번역해주세요",
            help="원하는 번역 스타일을 자유롭게 입력하세요."
        )
    else:
        # 커스텀 스타일이 선택되지 않은 경우 세션 상태 초기화
        if "custom_style_instruction" in st.session_state:
            st.session_state.custom_style_instruction = ""

    # 선택된 스타일들을 session_state에 저장
    selected_styles = []
    if style_literal:
        selected_styles.append(StyleTranslator.STYLE_LITERAL)
    if style_conversational:
        selected_styles.append(StyleTranslator.STYLE_CONVERSATIONAL)
    if style_business:
        selected_styles.append(StyleTranslator.STYLE_BUSINESS)
    if style_formal:
        selected_styles.append(StyleTranslator.STYLE_FORMAL)
    if style_concise:
        selected_styles.append(StyleTranslator.STYLE_CONCISE)

    st.session_state.selected_styles = selected_styles

    # 최소 하나는 선택해야 함
    if not selected_styles:
        st.sidebar.warning("⚠️ 최소 하나의 스타일을 선택해주세요.")

    st.sidebar.markdown("---")

    # 추가 옵션
    st.sidebar.markdown("**추가 옵션**")

    st.sidebar.checkbox(
        "🏷️ 고유명사 유지",
        value=False,
        key="preserve_proper_nouns",
        help="인명, 지명, 브랜드명 등을 원문 그대로 유지합니다."
    )

    st.sidebar.checkbox(
        "🔄 대안 표현 함께 보기",
        value=False,
        key="include_alternatives",
        help="각 스타일당 2-3개의 대안 표현을 추가로 제공합니다."
    )

    # 스타일 재생성 버튼
    if st.sidebar.button("🔄 스타일 재생성", use_container_width=True):
        if not selected_styles:
            st.sidebar.error("⚠️ 스타일을 하나 이상 선택해주세요.")
        else:
            regenerate_multi_style_translation()

    st.sidebar.markdown("---")

    # 정보 및 도움말 섹션
    st.sidebar.markdown("#### ℹ️ 정보 및 도움말")

    # 시스템 정보
    with st.sidebar.expander("🔧 시스템 정보", expanded=False):
        provider_display = "🔵 OpenAI" if provider == "openai" else "🟢 Azure OpenAI"
        st.markdown(f"**Provider:** {provider_display}")

    # 도움말
    with st.sidebar.expander("💡 도움말", expanded=False):
        st.markdown("""
        **🌐 자동 번역**
        입력하신 언어를 자동으로 감지하여 번역합니다.

        **📝 Markdown 지원**
        다음 Markdown 문법을 사용할 수 있습니다:
        - **볼드**, *이탤릭*, `코드`
        - [링크](URL)
        - 리스트 (- 또는 1.)
        - > 인용문
        - 표
        """)

    return selected_model_or_deployment, options


# ============================================================================
# UI Rendering Functions (UI 렌더링)
# ============================================================================

def show_title() -> None:
    """페이지 타이틀을 표시합니다.

    Config에서 APP_ICON과 APP_TITLE을 로드하여 표시합니다.
    """
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")


def render_input_area() -> st.delta_generator.DeltaGenerator:
    """입력 영역을 렌더링하고 통계 placeholder를 반환합니다.

    Config에서 TEXT_AREA_HEIGHT를 로드하여 텍스트 영역 높이를 설정합니다.

    Returns:
        통계를 표시할 placeholder
    """
    # 원문 입력 영역 - 타이틀과 통계를 좌우로 나누기
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**원문**")
    with col2:
        stats_placeholder = st.empty()

    # 입력 텍스트 영역
    st.text_area(
        "원문",
        placeholder="번역할 텍스트를 입력하세요... (한국어/English 자동 감지)",
        height=config.TEXT_AREA_HEIGHT,
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

    Config에서 MAX_INPUT_LENGTH를 로드하여 입력 길이를 검증합니다.

    Args:
        input_text: 입력 텍스트
        source_lang: 원본 언어
        target_lang: 대상 언어
        translation_manager: 번역 관리자 인스턴스
    """
    # 입력 길이 검증
    input_length = len(input_text)
    max_length = config.MAX_INPUT_LENGTH

    # 길이 초과 경고
    if input_length > max_length:
        st.error(
            f"⚠️ **입력 길이 제한 초과**: 현재 {input_length:,}자 / 최대 {max_length:,}자\n\n"
            f"입력 텍스트가 최대 길이를 {input_length - max_length:,}자 초과했습니다. "
            f"텍스트를 줄여주세요."
        )
    elif input_length > max_length * 0.8:  # 80% 이상이면 경고
        st.warning(
            f"⚠️ **입력 길이 주의**: 현재 {input_length:,}자 / 최대 {max_length:,}자\n\n"
            f"최대 길이에 가까워지고 있습니다. (남은 용량: {max_length - input_length:,}자)"
        )

    col_btn1, col_btn2 = st.columns([3, 1])

    with col_btn1:
        if st.button(
            "번역하기",
            type="primary",
            use_container_width=True
        ):
            handle_translation(input_text, source_lang, target_lang, translation_manager)

    with col_btn2:
        st.button("🗑️ 지우기", use_container_width=True, on_click=clear_inputs)


def render_translation_result() -> None:
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
            st.components.v1.html(  # type: ignore
                create_dual_copy_buttons(result, "translation"),
                height=60
            )
            # 포맷 유지 옵션에 따라 표시
            if st.session_state.preserve_format:
                formatted_result = format_translation_result(result)
                st.markdown(formatted_result)
            else:
                st.markdown(result)

        with tab2:
            # Markdown 원본 복사 버튼
            st.components.v1.html(  # type: ignore
                create_copy_button(result, "📋 Markdown 복사", "markdown"),
                height=50
            )
            st.code(result, language="markdown", line_numbers=False)

        # FEATURE-023: 다중 스타일 번역 결과 표시 (한국어→영어만)
        if st.session_state.multi_style_results:
            st.markdown("---")

            from components.style_translator import StyleTranslator

            multi_results = st.session_state.multi_style_results

            # 다중 스타일인 경우만 헤더 표시 (원문 유지만 선택한 경우 제외)
            is_single_literal = (len(multi_results) == 1 and StyleTranslator.STYLE_LITERAL in multi_results)

            if not is_single_literal:
                st.subheader("🎨 다양한 스타일 번역")

            # 각 스타일별로 세로 목록 표시
            for style_key, style_result in multi_results.items():
                # 스타일 레이블 가져오기
                style_label = StyleTranslator.STYLE_LABELS.get(style_key, style_key)

                # 스타일 제목 표시
                st.markdown(f"### {style_label}")

                # 결과가 딕셔너리인 경우 (include_alternatives=True)
                if isinstance(style_result, dict):
                    primary_translation = style_result.get("primary", "")
                    alternatives = style_result.get("alternatives", [])

                    # 주 번역 표시
                    st.markdown("**주 번역:**")
                    st.components.v1.html(  # type: ignore
                        create_copy_button(primary_translation, "📋 복사", f"style_{style_key}"),
                        height=50
                    )
                    st.markdown(primary_translation)

                    # 대안 표현 표시
                    if alternatives:
                        st.markdown("**대안 표현:**")
                        for idx, alt in enumerate(alternatives, 1):
                            st.markdown(f"{idx}. {alt}")
                            st.components.v1.html(  # type: ignore
                                create_copy_button(alt, "📋", f"alt_{style_key}_{idx}"),
                                height=50
                            )
                else:
                    # 결과가 문자열인 경우 (include_alternatives=False)
                    st.components.v1.html(  # type: ignore
                        create_copy_button(style_result, "📋 복사", f"style_{style_key}"),
                        height=50
                    )
                    st.markdown(style_result)

                st.markdown("")  # 스타일 간 간격


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
        language_detector: 언어 감지기 ���스턴스
        text_analyzer: 텍스트 분석기 인스턴스
        selected_model: 선택된 모델명

    Returns:
        (source_lang, target_lang, direction_arrow) 튜플
    """
    max_length = config.MAX_INPUT_LENGTH

    if input_text:
        # 언어 감지 및 번역 방향 결정
        source_lang, target_lang, direction_arrow = language_detector.get_translation_direction(input_text)

        # 통계 계산
        text_analyzer.model = selected_model
        input_length = len(input_text)
        token_count = text_analyzer.count_tokens(input_text)

        # 색상 결정
        length_color = "#888"
        if input_length > max_length:
            length_color = "#ff4444"  # 빨간색: 초과
        elif input_length > max_length * 0.8:
            length_color = "#ff8800"  # 주황색: 경고

        # 통합된 통계 표시 HTML 생성
        stats_html = f"<div style='text-align: right; color: {length_color};'>{input_length:,} / {max_length:,}자 <span style='font-size: 0.85em;'>({token_count:,} 토큰)</span></div>"  # noqa: E501

        stats_placeholder.markdown(stats_html, unsafe_allow_html=True)
    else:
        source_lang = "unknown"
        target_lang = "unknown"
        direction_arrow = ""
        stats_placeholder.markdown(
            f"<div style='text-align: right; color: #888;'>0자 / 0 토큰<br/><span style='font-size: 0.9em;'>입력: 0 / {max_length:,}자</span></div>",  # noqa: E501
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

    # 최대 길이 검증
    max_length = config.MAX_INPUT_LENGTH
    if len(input_text) > max_length:
        st.error(
            f"⚠️ **입력 길이 제한 초과**\n\n"
            f"입력 텍스트가 최대 길이를 초과했습니다.\n"
            f"- 현재: {len(input_text):,}자\n"
            f"- 최대: {max_length:,}자\n"
            f"- 초과: {len(input_text) - max_length:,}자\n\n"
            f"텍스트를 줄여주세요."
        )
        return

    if source_lang == "unknown" or target_lang == "unknown":
        st.error("언어를 감지할 수 없습니다. 한국어 또는 영어 텍스트를 입력해주세요.")
        return

    with st.spinner("번역 중..."):
        try:
            result = translation_manager.translate(
                input_text,
                source_lang,
                target_lang,
                st.session_state.session_id
            )
            st.session_state.translation_result = {
                "text": result,
                "source": source_lang,
                "target": target_lang
            }
            # FEATURE-023: 번역 완료 상태 업데이트
            st.session_state.translation_completed = True
            st.session_state.source_language = source_lang
            st.session_state.target_language = target_lang

            # FEATURE-024: 양방향 번역(한↔영) 모두 다중 스타일 번역 수행
            from components.style_translator import StyleTranslator

            # StyleTranslator 인스턴스 생성
            style_translator = StyleTranslator(
                client=translation_manager.client,
                model=translation_manager.model,
                temperature=0.3,
                max_tokens=2000,
                timeout=30
            )

            # 사용자가 선택한 스타일 사용 (최소 1개 이상)
            selected_styles = st.session_state.selected_styles
            if not selected_styles:
                # 기본값: 직역 스타일
                selected_styles = [StyleTranslator.STYLE_LITERAL]

            # 다중 스타일 번역 수행
            preserve_proper_nouns = st.session_state.get("preserve_proper_nouns", False)
            include_alternatives = st.session_state.get("include_alternatives", False)
            custom_instruction = st.session_state.get("custom_style_instruction", "")

            # 커스텀 지침이 있으면 각 스타일마다 개별 번역
            if custom_instruction.strip():
                multi_style_results = {}
                for style in selected_styles:
                    translation = style_translator.translate_single_style(
                        text=input_text,
                        style=style,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        preserve_proper_nouns=preserve_proper_nouns,
                        custom_instruction=custom_instruction
                    )

                    if include_alternatives:
                        alternatives = style_translator._generate_alternatives(
                            text=input_text,
                            base_translation=translation,
                            style=style,
                            source_lang=source_lang,
                            target_lang=target_lang
                        )
                        multi_style_results[style] = {
                            "primary": translation,
                            "alternatives": alternatives
                        }
                    else:
                        multi_style_results[style] = translation
            else:
                # 일반 다중 스타일 번역
                multi_style_results = style_translator.translate_multi_style(
                    text=input_text,
                    styles=selected_styles,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    preserve_proper_nouns=preserve_proper_nouns,
                    include_alternatives=include_alternatives
                )

            # 결과 저장
            st.session_state.multi_style_results = multi_style_results

        except Exception as e:
            st.error(f"번역 중 오류가 발생했습니다: {str(e)}")


def regenerate_multi_style_translation() -> None:
    """선택된 스타일로 다중 스타일 번역을 재생성합니다.

    사용자가 스타일 옵션을 변경한 후 재생성 버튼을 클릭했을 때 호출됩니다.
    """
    # 번역 결과가 없으면 에러
    if not st.session_state.translation_result:
        st.error("먼저 번역을 수행해주세요.")
        return

    # 한국어→영어가 아니면 에러
    source_lang = st.session_state.source_language
    target_lang = st.session_state.target_language
    if source_lang != "Korean" or target_lang != "English":
        st.error("다중 스타일 번역은 한국어→영어에서만 지원됩니다.")
        return

    # 입력 텍스트 가져오기
    input_text = st.session_state.input_text
    if not input_text:
        st.error("입력 텍스트가 없습니다.")
        return

    # 선택된 스타일 가져오기
    selected_styles = st.session_state.selected_styles
    if not selected_styles:
        st.error("최소 하나의 스타일을 선택해주세요.")
        return

    # API 클라이언트와 모델 정보 가져오기
    client = st.session_state.get("api_client")
    model = st.session_state.get("selected_model")
    if not client or not model:
        st.error("API 클라이언트 정보를 찾을 수 없습니다.")
        return

    with st.spinner("스타일 재생성 중..."):
        try:
            from components.style_translator import StyleTranslator

            # StyleTranslator 인스턴스 생성
            style_translator = StyleTranslator(
                client=client,
                model=model,
                temperature=0.3,
                max_tokens=2000,
                timeout=30
            )

            # 옵션 가져오기
            preserve_proper_nouns = st.session_state.get("preserve_proper_nouns", False)
            include_alternatives = st.session_state.get("include_alternatives", False)
            custom_instruction = st.session_state.get("custom_style_instruction", "")

            # 커스텀 지침이 있으면 모든 스타일에 적용
            if custom_instruction.strip():
                multi_style_results = {}
                for style in selected_styles:
                    translation = style_translator.translate_single_style(
                        text=input_text,
                        style=style,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        preserve_proper_nouns=preserve_proper_nouns,
                        custom_instruction=custom_instruction
                    )

                    if include_alternatives:
                        alternatives = style_translator._generate_alternatives(
                            text=input_text,
                            base_translation=translation,
                            style=style,
                            source_lang=source_lang,
                            target_lang=target_lang
                        )
                        multi_style_results[style] = {
                            "primary": translation,
                            "alternatives": alternatives
                        }
                    else:
                        multi_style_results[style] = translation
            else:
                # 일반 다중 스타일 번역
                multi_style_results = style_translator.translate_multi_style(
                    text=input_text,
                    styles=selected_styles,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    preserve_proper_nouns=preserve_proper_nouns,
                    include_alternatives=include_alternatives
                )

            # 결과 저장
            st.session_state.multi_style_results = multi_style_results
            st.success("✅ 스타일 재생성 완료!")

        except Exception as e:
            st.error(f"스타일 재생성 중 오류가 발생했습니다: {str(e)}")


# ============================================================================
# Main Function
# ============================================================================

def main() -> None:
    """메인 애플리케이션 함수"""
    # 1. 페이지 설정 및 초기화
    initialize_page_config()
    initialize_session_state()

    # 세션 ID 생성 (Langfuse 추적용)
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # 2. 타이틀 표시
    show_title()

    # 3. API 클라이언트 및 컴포넌트 초기화
    client, provider = setup_api_client()
    language_detector, text_analyzer = initialize_components()

    # 4. 사이드바 설정 및 번역 관리자 초기화
    selected_model_or_deployment, _ = setup_sidebar(provider)

    # FEATURE-023: API 클라이언트 및 모델 정보를 session_state에 저장 (스타일 재생성 버튼용)
    st.session_state.api_client = client

    # Factory 패턴으로 TranslationManager 생성
    from components.translation import TranslationManagerFactory

    if provider == "azure":
        # Azure: deployment 및 model 파라미터 전달
        # deployment → model 역매핑 (SUPPORTED_DEPLOYMENTS에서 찾기)
        from components.translation import AzureTranslationManager
        model_name = None
        for model, deployment in AzureTranslationManager.SUPPORTED_DEPLOYMENTS.items():
            if deployment == selected_model_or_deployment:
                model_name = model
                break

        translation_manager = TranslationManagerFactory.create(
            provider=provider,
            client=client,
            deployment=selected_model_or_deployment,
            model=model_name  # 실제 모델명 전달
        )
        # FEATURE-023: 실제 모델명 저장
        st.session_state.selected_model = model_name if model_name else selected_model_or_deployment
    else:
        # OpenAI: model 파라미터 전달
        translation_manager = TranslationManagerFactory.create(
            provider=provider,
            client=client,
            model=selected_model_or_deployment
        )
        # FEATURE-023: 모델명 저장
        st.session_state.selected_model = selected_model_or_deployment

    # 5. 입력 영역 렌더링
    stats_placeholder = render_input_area()

    # 6. 통계 업데이트 및 언어 감지
    input_text = st.session_state.input_text
    source_lang, target_lang, _ = update_statistics(
        input_text,
        stats_placeholder,
        language_detector,
        text_analyzer,
        translation_manager.model  # TranslationManager의 model 속성 사용
    )

    # 7. 액션 버튼 렌더링
    render_action_buttons(input_text, source_lang, target_lang, translation_manager)

    # 8. 번역 결과 표시
    render_translation_result()


if __name__ == "__main__":
    main()
