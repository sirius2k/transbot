Feature: 페이지 렌더링
  Streamlit 앱의 기본 UI 요소가 정상적으로 렌더링되는지 확인하는 Smoke Test

  Background:
    Given Streamlit 앱이 "http://localhost:8501"에서 실행 중

  Scenario: 기본 페이지 로딩 및 타이틀 표시
    When 브라우저에서 앱에 접속
    Then 페이지가 3초 이내에 로드됨
    And 타이틀 "TransBot"이 표시됨
    And 브라우저 탭 제목이 "TransBot"으로 표시됨
    And 로딩 스피너가 사라지고 메인 화면이 표시됨

  Scenario: 입력 영역 렌더링
    Given 페이지가 정상적으로 로드됨
    When 메인 화면을 확인
    Then "원문" 레이블이 표시됨
    And 텍스트 입력 필드가 렌더링됨
    And Placeholder "번역할 텍스트를 입력하세요"가 표시됨
    And 입력 필드가 빈 상태로 초기화됨
    And 통계 정보 영역이 표시됨

  Scenario: 사이드바 렌더링 (OpenAI Provider)
    Given ".env" 파일에 "AI_PROVIDER=openai" 설정됨
    And 페이지가 정상적으로 로드됨
    When 사이드바를 확인
    Then 사이드바가 화면 왼쪽에 표시됨
    And "⚙️ 설정" 헤더가 표시됨
    And "AI 모델 선택" 섹션이 표시됨
    And 모델 선택 드롭다운이 렌더링됨
    And "번역 옵션" 섹션이 표시됨
    And Help 섹션이 표시됨

  Scenario: 액션 버튼 표시
    Given 페이지가 정상적으로 로드됨
    When 입력 영역 하단을 확인
    Then "🚀 번역" 버튼이 표시됨
    And "🗑️ 지우기" 버튼이 표시됨
    And 두 버튼이 좌우로 배치됨
    And 버튼이 클릭 가능한 상태임
