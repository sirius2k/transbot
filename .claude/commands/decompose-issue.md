# 작업 세분화하기

너는 이제부터 작업(Task)를 세분화하는 전략 전문가야. 아래 작업을 독립적인 여러 개의 이슈로 분해하는 작업을 해줘.

## 세분화할 작업

$ARGUMENTS

## 작업 순서

1. **작업 분석:** 작업의 핵심 요구사항과 목표를 이해하기.
2. **작업 분해:** 주요 작업을 더 작고 관리하기 쉬운 하위 작업 또는 이슈로 나누기.
3. **의존성 분석:** 다른 작업이 선행되야 하는 의존성 파악하기
4. **분해된 이슈 출력:** 분해된 이슈들을 출력하기.
5. **GitHub에 이슈를 생성할지 묻기:** GitHub에 이 이슈들을 공식적으로 생성할지 여부를 사용자가 결정하도록 요청하기.

## 이슈 템플릿

<github_issue_template>

---
title: [작업 유형] 명확하고 실행 가능한 제목
labels:

- type:bug|type:enhancement|type:docs|type:question|type:security|type:performance
- priority:critical|priority:high|priority:medium|priority:low
- status:wontfix|status:duplicate|status:invalid|status:blocked|status:in-progress
- contrib:good-first-issue|contrib:help-wanted

---

## 설명

[무엇을 해야하고 왜 해야 하는지]

## 작업 유형

- [ ] 버그 수정
- [ ] 기능 개선/추가
- [ ] 문서화
- [ ] 질문
- [ ] 보안 관련
- [ ] 성능 관련

## 완료 조건

- [ ] 특정 요구사항 1
- [ ] 특정 요구사항 2
- [ ] 테스트 통과
- [ ] 린팅 통과
- [ ] 문서 업데이트 (해당하는 경우)

## 구현 참고사항

### 수정할 파일

- `path/to/file1` - [무엇을 변경할지]
- `path/to/file2` - [무엇을 변경할지]

### 시술적 고려사항

- [주의할 점 또는 고려사항]
- [성능 영행]
- [보안 고려사항]

## 의존성

- [ ] 없음
- [ ] 이슈 #[번호]가 먼저 완료되어야 함
- [ ] [외부 의존성] 필요

## 예상 소요 시간

[이 태스크를 작업하는데 예상되는 소요 시간]

</github_issue_template>
