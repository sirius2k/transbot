# 범용 가이드 (General Guides)

이 디렉토리는 **TransBot 프로젝트에 특화되지 않은 범용 가이드**를 보관합니다.

## 📚 가이드 목록

### [Claude 기반 개발 프로젝트 가이드라인](claude-development-guide.md)

- **대상**: 모든 Claude AI 협업 프로젝트
- **목적**: Claude와 효과적으로 협업하는 프로젝트 구성 방법
- **내용**:
  - 프로젝트 구조 권장사항
  - CLAUDE.md 작성 가이드
  - `.claude/` 디렉토리 활용법
  - 프롬프트 템플릿 관리
  - 권한 관리 전략
- **특징**: TransBot을 예시로 사용하여 설명하지만, 다른 프로젝트에도 적용 가능

### [Claude 기반 개발 프로젝트 가이드라인 - CoT](claude-development-guide-cot.md)

- **대상**: 가이드 작성자, 아키텍트
- **목적**: 위 가이드를 작성한 사고 과정(Chain of Thought) 기록
- **내용**:
  - TransBot 프로젝트 분석 과정
  - 패턴 추출 방법론
  - 가이드라인 도출 근거
- **특징**: 메타 문서로, 다른 가이드를 작성할 때 참고 가능

## 🎯 사용 시나리오

### 1. 새로운 Claude 프로젝트 시작 시

`claude-development-guide.md`를 참고하여 프로젝트 구조를 설계합니다.

```bash
# 새 프로젝트에 적용
cd your-new-project/
mkdir -p .claude/commands docs/guides
# 가이드를 참고하여 CLAUDE.md 작성
```

### 2. TransBot 개발 시

이 디렉토리가 아닌 **상위 디렉토리의 특화 가이드**를 사용합니다:

- [development/](../development/) - 개발 가이드
- [infrastructure/](../infrastructure/) - 인프라 가이드
- [quality/](../quality/) - 품질 가이드
- [workflows/](../workflows/) - 워크플로우 가이드

### 3. 가이드 작성 방법론 학습 시

`claude-development-guide-cot.md`를 읽고 가이드 작성 사고 과정을 이해합니다.

## ⚠️ 주의사항

- 이 디렉토리의 가이드는 **참고용**입니다
- TransBot 실제 개발 작업 시에는 **프로젝트 특화 가이드**를 우선 사용하세요
- 두 가이드의 내용이 충돌하는 경우, **프로젝트 특화 가이드**가 우선입니다

---

마지막 업데이트: 2026-01-31
