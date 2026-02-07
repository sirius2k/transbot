Feature: 에러 핸들링
  사용자가 잘못된 입력이나 예외 상황을 발생시켰을 때 앱이 적절한 에러 메시지를 표시하는지 검증한다.

  Background:
    Given Streamlit 앱이 "http://localhost:8501"에서 실행 중
    And 페이지가 정상적으로 로드됨

  Scenario: 입력 길이 초과 에러
    When 사용자가 50001자의 매우 긴 텍스트를 입력
    Then "입력 길이 제한 초과" 에러 메시지가 표시됨

  Scenario: 입력 길이 경고 (80% 이상)
    When 사용자가 40000자의 긴 텍스트를 입력
    Then "입력 길이 주의" 경고 메시지가 표시됨

  Scenario: 스타일 미선택 경고
    Given 사이드바가 열려 있음
    When 모든 스타일 체크박스를 해제
    Then "최소 하나의 스타일을 선택해주세요" 경고 메시지가 표시됨
