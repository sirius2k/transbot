import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()

st.set_page_config(
    page_title="영어-한국어 번역기",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 영어-한국어 번역기")

# API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if not api_key:
        st.warning("OpenAI API 키를 입력해주세요.")
        st.stop()

client = OpenAI(api_key=api_key)

# 사이드바 - 모델 선택
st.sidebar.header("⚙️ 설정")
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

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """텍스트의 토큰 수를 계산합니다."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def detect_language(text: str) -> str:
    """텍스트의 언어를 자동 감지합니다. (한글/영어)"""
    if not text or not text.strip():
        return "unknown"

    # 한글 문자 확인 (가-힣)
    korean_chars = sum(1 for char in text if '\uac00' <= char <= '\ud7a3')
    # 영문 알파벳 확인
    english_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)

    # 전체 알파벳 문자 수
    total_alpha = korean_chars + english_chars

    if total_alpha == 0:
        return "unknown"

    # 한글이 50% 이상이면 한국어, 아니면 영어
    if korean_chars / total_alpha > 0.5:
        return "Korean"
    else:
        return "English"

# 자동 언어 감지 모드
st.info("🌐 **자동 번역**: 입력하신 언어를 자동으로 감지하여 번역합니다.")

st.info("💡 **Markdown 지원**: **볼드**, *이탤릭*, `코드`, [링크](URL), 리스트(- 또는 1.), > 인용문, 표 등 사용 가능")

# 원문 입력 영역 - 타이틀과 통계를 좌우로 나누기
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**원문 (Markdown 지원)**")
with col2:
    stats_placeholder = st.empty()

# 입력 텍스트 영역
input_text = st.text_area("원문", placeholder="번역할 텍스트를 입력하세요... (한국어/English 자동 감지)", height=200, label_visibility="collapsed")

# 언어 자동 감지 및 통계 업데이트
if input_text:
    detected_lang = detect_language(input_text)
    char_count = len(input_text)
    token_count = count_tokens(input_text, selected_model)

    # 감지된 언어에 따라 번역 방향 설정
    if detected_lang == "Korean":
        source_lang = "Korean"
        target_lang = "English"
        direction_arrow = "🇰🇷 → 🇺🇸"
    elif detected_lang == "English":
        source_lang = "English"
        target_lang = "Korean"
        direction_arrow = "🇺🇸 → 🇰🇷"
    else:
        source_lang = "unknown"
        target_lang = "unknown"
        direction_arrow = "❓"

    stats_placeholder.markdown(
        f"<div style='text-align: right;'>{direction_arrow}<br/>{char_count:,}자 / {token_count:,} 토큰</div>",
        unsafe_allow_html=True
    )
else:
    source_lang = "unknown"
    target_lang = "unknown"
    stats_placeholder.markdown("<div style='text-align: right; color: #888;'>0자 / 0 토큰</div>", unsafe_allow_html=True)

def translate(text: str, source: str, target: str, model: str) -> str:
    """OpenAI API를 사용하여 텍스트를 번역합니다."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following {source} text to {target}. IMPORTANT: Preserve all Markdown formatting (bold, italic, headings, lists, links, code blocks, blockquotes, tables, etc.) in the translation. Only respond with the translation, nothing else."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# 번역 버튼
if st.button("번역하기", type="primary", use_container_width=True):
    if input_text.strip():
        if source_lang == "unknown" or target_lang == "unknown":
            st.error("언어를 감지할 수 없습니다. 한국어 또는 영어 텍스트를 입력해주세요.")
        else:
            with st.spinner("번역 중..."):
                try:
                    result = translate(input_text, source_lang, target_lang, selected_model)

                    # 번역 방향 표시
                    direction_text = f"{source_lang} → {target_lang}"
                    st.subheader(f"번역 결과 ({direction_text})")

                    # 탭으로 렌더링 뷰와 Markdown 원본 제공
                    tab1, tab2 = st.tabs(["📄 렌더링", "📝 Markdown 원본"])

                    with tab1:
                        st.markdown(result)

                    with tab2:
                        st.code(result, language="markdown", line_numbers=False)

                except Exception as e:
                    st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
    else:
        st.warning("번역할 텍스트를 입력해주세요.")
