#!/usr/bin/env python3
"""Langfuse에서 최근 번역 요청의 프롬프트를 분석하는 스크립트

최근 3건의 번역 trace를 조회하고 각 요청의:
- 번역 방향 (한→영, 영→한)
- 적용된 스타일 (literal, conversational, business 등)
- 프롬프트 구조 (system message, style instruction)
를 비교 분석합니다.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from langfuse import Langfuse
except ImportError:
    print("❌ Langfuse SDK가 설치되지 않았습니다.")
    print("   다음 명령으로 설치하세요: pip install langfuse")
    sys.exit(1)

from config import Config


def extract_style_instruction(system_message: str) -> Optional[str]:
    """System message에서 STYLE INSTRUCTION 부분을 추출합니다.

    Args:
        system_message: System prompt 전체 텍스트

    Returns:
        STYLE INSTRUCTION 내용, 없으면 None
    """
    if "STYLE INSTRUCTION:" not in system_message:
        return None

    # "STYLE INSTRUCTION:" 이후부터 다음 섹션 전까지 추출
    start = system_message.find("STYLE INSTRUCTION:") + len("STYLE INSTRUCTION:")

    # "Only respond with" 또는 "\n\n" 이전까지
    end_markers = ["Only respond with", "\n\nIMPORTANT:", "\n\n"]
    end = len(system_message)

    for marker in end_markers:
        marker_pos = system_message.find(marker, start)
        if marker_pos != -1:
            end = min(end, marker_pos)

    instruction = system_message[start:end].strip()
    return instruction


def extract_translation_direction(system_message: str) -> str:
    """System message에서 번역 방향을 추출합니다.

    Args:
        system_message: System prompt 전체 텍스트

    Returns:
        번역 방향 (예: "Korean→English", "English→Korean")
    """
    # "Translate the following {source_lang} text to {target_lang}" 패턴 찾기
    if "Korean text to English" in system_message:
        return "Korean → English"
    elif "English text to Korean" in system_message:
        return "English → Korean"
    else:
        # 패턴 매칭으로 추출 시도
        import re
        pattern = r"Translate the following (\w+) text to (\w+)"
        match = re.search(pattern, system_message)
        if match:
            return f"{match.group(1)} → {match.group(2)}"

    return "Unknown"


def analyze_trace(trace: Any, langfuse: Langfuse) -> Dict[str, Any]:
    """단일 trace를 분석합니다.

    Args:
        trace: Langfuse trace 객체
        langfuse: Langfuse 클라이언트 (observation 조회용)

    Returns:
        분석 결과 딕셔너리
    """
    result = {
        "trace_id": trace.id,
        "timestamp": trace.timestamp,
        "direction": "Unknown",
        "style": "Unknown",
        "style_instruction": None,
        "user_message": None,
        "system_message": None
    }

    # Trace의 observations는 ID 리스트일 수 있으므로, 직접 조회
    # fetch_trace를 사용하여 전체 데이터 가져오기
    try:
        fetch_response = langfuse.fetch_trace(trace.id)
        # FetchTraceResponse.data에 실제 trace 데이터가 있음
        full_trace = fetch_response.data if hasattr(fetch_response, 'data') else fetch_response
    except Exception as e:
        print(f"⚠️  Trace {trace.id} 조회 실패: {e}")
        return result

    # observations 확인
    if hasattr(full_trace, 'observations') and full_trace.observations:
        for obs in full_trace.observations:
            # obs가 문자열(ID)인 경우 건너뛰기
            if isinstance(obs, str):
                continue

            if not hasattr(obs, 'type'):
                continue

            if obs.type == "GENERATION":
                # name 확인 (translation vs style translation)
                obs_name = getattr(obs, 'name', None)

                # Input에서 messages 추출
                if hasattr(obs, 'input') and obs.input:
                    messages = obs.input

                    # messages가 딕셔너리 형태일 수 있음
                    if isinstance(messages, dict) and 'messages' in messages:
                        messages = messages['messages']

                    # messages 리스트에서 system과 user 메시지 추출
                    if isinstance(messages, list):
                        for msg in messages:
                            if isinstance(msg, dict):
                                role = msg.get('role')
                                content = msg.get('content', '')

                                if role == 'system':
                                    result['system_message'] = content
                                    result['direction'] = extract_translation_direction(content)
                                    result['style_instruction'] = extract_style_instruction(content)
                                elif role == 'user':
                                    result['user_message'] = content

                # style translation generation인 경우 표시
                if obs_name:
                    result['generation_name'] = obs_name

                # Metadata에서 추가 정보 추출
                if hasattr(obs, 'metadata') and obs.metadata:
                    metadata = obs.metadata
                    if isinstance(metadata, dict):
                        if 'direction' in metadata:
                            result['direction'] = metadata['direction']

                        # 스타일 정보는 metadata에 없을 수 있음
                        # style_instruction에서 유추

                break  # 첫 번째 generation만 분석

    # Style 추정 (style_instruction 기반)
    if result['style_instruction']:
        instruction_lower = result['style_instruction'].lower()
        if 'conversational' in instruction_lower or '구어체' in instruction_lower:
            result['style'] = 'conversational'
        elif 'business' in instruction_lower or '비즈니스' in instruction_lower:
            result['style'] = 'business'
        elif 'formal' in instruction_lower or '공식' in instruction_lower or '격식' in instruction_lower:
            result['style'] = 'formal'
        elif 'literal' in instruction_lower or '직역' in instruction_lower:
            result['style'] = 'literal'
        elif 'concise' in instruction_lower or '간결' in instruction_lower:
            result['style'] = 'concise'

    return result


def print_analysis_report(analyses: List[Dict[str, Any]]) -> None:
    """분석 결과를 출력합니다.

    Args:
        analyses: 분석 결과 리스트
    """
    print("\n" + "="*80)
    print("📊 Langfuse 프롬프트 분석 결과")
    print("="*80 + "\n")

    for i, analysis in enumerate(analyses, 1):
        timestamp = analysis['timestamp']
        if timestamp:
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_str = "Unknown"

        print(f"[Trace {i}] - {timestamp_str}")
        print(f"  Trace ID: {analysis['trace_id']}")
        print(f"  📍 번역 방향: {analysis['direction']}")
        print(f"  🎨 스타일: {analysis['style']}")

        if analysis['user_message']:
            user_msg_preview = analysis['user_message'][:100]
            if len(analysis['user_message']) > 100:
                user_msg_preview += "..."
            print(f"  📝 원문: {user_msg_preview}")

        if analysis['style_instruction']:
            print(f"  📋 STYLE INSTRUCTION:")
            # 들여쓰기를 추가해서 출력
            instruction_lines = analysis['style_instruction'].split('\n')
            for line in instruction_lines:
                print(f"     {line}")
        else:
            print(f"  📋 STYLE INSTRUCTION: (없음)")

        print()

    # 차이점 분석
    print("-"*80)
    print("🔍 차이점 분석")
    print("-"*80 + "\n")

    # 번역 방향별 그룹화
    directions = {}
    for analysis in analyses:
        direction = analysis['direction']
        if direction not in directions:
            directions[direction] = []
        directions[direction].append(analysis)

    print(f"번역 방향별 분포:")
    for direction, items in directions.items():
        print(f"  - {direction}: {len(items)}건")
    print()

    # 스타일별 그룹화
    styles = {}
    for analysis in analyses:
        style = analysis['style']
        if style not in styles:
            styles[style] = []
        styles[style].append(analysis)

    print(f"스타일별 분포:")
    for style, items in styles.items():
        print(f"  - {style}: {len(items)}건")
    print()

    # 프롬프트 구조 차이
    print("프롬프트 구조 특징:")
    for direction, items in directions.items():
        if len(items) > 0:
            sample = items[0]
            if sample['style_instruction']:
                lang = "한국어" if "한국어" in sample['style_instruction'] else "English"
                print(f"  - {direction}: {lang} 지침 사용")

    print()


def main():
    """메인 함수"""
    # Config 로드
    config = Config.load()

    # Langfuse 설정 확인
    if not config.LANGFUSE_PUBLIC_KEY or not config.LANGFUSE_SECRET_KEY or not config.LANGFUSE_HOST:
        print("❌ Langfuse 설정이 누락되었습니다.")
        print("   .env 파일에 다음 환경 변수를 설정하세요:")
        print("   - LANGFUSE_PUBLIC_KEY")
        print("   - LANGFUSE_SECRET_KEY")
        print("   - LANGFUSE_HOST")
        sys.exit(1)

    print("🔍 Langfuse에서 최근 번역 요청을 조회하고 있습니다...\n")

    # Langfuse 클라이언트 초기화
    try:
        langfuse = Langfuse(
            public_key=config.LANGFUSE_PUBLIC_KEY,
            secret_key=config.LANGFUSE_SECRET_KEY,
            host=config.LANGFUSE_HOST
        )
    except Exception as e:
        print(f"❌ Langfuse 클라이언트 초기화 실패: {e}")
        sys.exit(1)

    # 더 많은 trace를 조회해서 스타일 번역 찾기 (최대 20건)
    try:
        traces = langfuse.fetch_traces(limit=20)
    except Exception as e:
        print(f"❌ Trace 조회 실패: {e}")
        sys.exit(1)

    if not traces.data or len(traces.data) == 0:
        print("⚠️  조회된 trace가 없습니다.")
        print("   TransBot에서 번역을 수행한 후 다시 시도하세요.")
        sys.exit(0)

    # 각 trace 분석 (스타일 번역이 있는 trace만 필터링)
    all_analyses = []
    style_analyses = []

    for trace in traces.data:
        analysis = analyze_trace(trace, langfuse)
        all_analyses.append(analysis)

        # 스타일 번역인 경우 (style_instruction이 있는 경우)
        if analysis['style_instruction']:
            style_analyses.append(analysis)

    # 스타일 번역이 있으면 우선 표시, 없으면 일반 번역 표시
    if len(style_analyses) >= 3:
        analyses = style_analyses[:3]
        print(f"✅ 스타일 번역 {len(style_analyses)}건 중 최근 3건을 분석합니다.\n")
    else:
        analyses = all_analyses[:3]
        if len(style_analyses) > 0:
            print(f"⚠️  스타일 번역 {len(style_analyses)}건만 발견되었습니다.")
            print(f"   일반 번역 포함 총 {len(all_analyses)}건 중 최근 3건을 분석합니다.\n")
        else:
            print("⚠️  스타일 번역이 발견되지 않았습니다.")
            print("   일반 번역 3건을 분석합니다.\n")
            print("💡 팁: TransBot 앱에서 '번역 스타일 옵션'을 선택하여 번역하면")
            print("      스타일별 프롬프트 차이를 분석할 수 있습니다.\n")

    # 결과 출력
    print_analysis_report(analyses)

    print("="*80)
    print("✅ 분석 완료")
    print("="*80)


if __name__ == "__main__":
    main()
