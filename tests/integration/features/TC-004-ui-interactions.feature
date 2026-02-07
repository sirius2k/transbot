Feature: UI 인터랙션
  사용자가 TransBot의 UI 요소(버튼, 체크박스, 입력 필드 등)와 상호작용할 때 예상대로 동작하는지 검증한다.

  Background:
    Given Streamlit 앱이 "http://localhost:8501"에서 실행 중
    And 페이지가 정상적으로 로드됨

  Scenario: 지우기 버튼 동작
    When 사용자가 "Hello World" 텍스트를 입력
    And "🗑️ 지우기" 버튼을 클릭
    Then 입력 필드가 비워짐
    And "0자" 텍스트가 표시됨

  Scenario: 번역 버튼 표시
    When 메인 화면을 확인
    Then "번역하기" 버튼이 표시됨

  Scenario: 사이드바 체크박스 선택
    Given 사이드바가 열려 있음
    When "📱 자연스러운 구어체" 체크박스를 선택
    Then "자연스러운 구어체" 체크박스가 선택됨

  Scenario: 여러 스타일 체크박스 선택
    Given 사이드바가 열려 있음
    When "📱 자연스러운 구어체" 체크박스를 선택
    And "📋 공식/문서용" 체크박스를 선택
    Then "자연스러운 구어체" 체크박스가 선택됨
    And "공식/문서용" 체크박스가 선택됨

  Scenario: 입력 필드 포커스 및 입력
    When 입력 필드를 클릭
    And 사용자가 "Test input" 텍스트를 입력
    Then 입력 필드에 "Test input" 텍스트가 표시됨
    And 통계 정보가 실시간으로 표시됨
