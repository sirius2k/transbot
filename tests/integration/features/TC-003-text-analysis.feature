Feature: 텍스트 분석 및 통계
  입력 텍스트의 언어를 자동으로 감지하고, 글자 수와 토큰 수 통계가 실시간으로 정확하게 표시되는지 확인한다.

  Background:
    Given Streamlit 앱이 "http://localhost:8501"에서 실행 중
    And 페이지가 정상적으로 로드됨

  Scenario: 영어 텍스트 언어 감지
    When 사용자가 "Hello, how are you today?" 텍스트를 입력
    Then 통계 정보가 실시간으로 표시됨
    And 글자 수 "28"이 표시됨
    And 토큰 수가 표시됨

  Scenario: 한국어 텍스트 언어 감지
    When 사용자가 "안녕하세요, 오늘 날씨가 좋네요." 텍스트를 입력
    Then 통계 정보가 실시간으로 표시됨
    And 글자 수 "18"이 표시됨
    And 토큰 수가 표시됨

  Scenario: 빈 텍스트 입력
    When 입력 필드를 비움
    Then "0자" 텍스트가 표시됨

  Scenario: 특수 문자 포함 텍스트
    When 사용자가 "Hello! 123 테스트@#$" 텍스트를 입력
    Then 통계 정보가 실시간으로 표시됨
    And 토큰 수가 표시됨
