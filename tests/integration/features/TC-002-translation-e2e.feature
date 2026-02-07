Feature: 번역 E2E 플로우
  사용자가 텍스트를 입력하고 번역 버튼을 클릭하여 번역 결과를 받는 전체 E2E 플로우 검증.
  양방향 번역(영어↔한국어), Markdown 포맷 보존, 다중 스타일 번역이 정상적으로 동작하는지 확인한다.

  Background:
    Given Streamlit 앱이 "http://localhost:8501"에서 실행 중
    And 페이지가 정상적으로 로드됨

  Scenario: 영어 → 한국어 번역
    Given 입력 필드가 빈 상태임
    When 사용자가 "Hello, how are you today?" 텍스트를 입력
    And "번역하기" 버튼을 클릭
    Then 번역 결과 섹션이 표시됨
    And 번역 결과에 "안녕" 텍스트가 포함됨
    And 언어 감지 결과가 "English"로 표시됨

  Scenario: 한국어 → 영어 번역
    Given 입력 필드가 빈 상태임
    When 사용자가 "안녕하세요, 오늘 날씨가 좋네요." 텍스트를 입력
    And "번역하기" 버튼을 클릭
    Then 번역 결과 섹션이 표시됨
    And 언어 감지 결과가 "Korean"로 표시됨
    And 통계 정보가 표시됨

  Scenario: Markdown 포맷 보존 번역
    Given "원문 유지" 옵션이 체크됨
    When 사용자가 Markdown 텍스트를 입력
    And "번역하기" 버튼을 클릭
    Then 번역 결과 섹션이 표시됨
    And 번역 결과에 "#" 문자가 포함됨
    And 번역 결과에 "**" 문자가 포함됨
    And 원문과 번역 결과가 함께 표시됨

  Scenario: 다중 스타일 번역
    Given "자연스러운 구어체" 스타일이 선택됨
    And "공식/문서용" 스타일이 선택됨
    When 사용자가 "안녕하세요, 내일까지 보고서를 제출해주세요." 텍스트를 입력
    And "번역하기" 버튼을 클릭
    Then 번역 결과 섹션이 표시됨
    And "자연스러운 구어체" 스타일 번역이 표시됨
    And "공식/문서용" 스타일 번역이 표시됨
    And 두 스타일이 명확히 구분되어 표시됨
