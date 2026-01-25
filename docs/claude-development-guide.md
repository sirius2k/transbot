# Claude 기반 개발 프로젝트 가이드라인

- 작성자: TransBot Development Team
- 버전: 1.0
- 최초 작성일: 2026년 1월 25일

---

## 1. 개요

이 문서는 Claude AI와 효과적으로 협업하는 개발 프로젝트를 구성하기 위한 가이드라인입니다. TransBot 프로젝트의 실제 경험을 바탕으로 작성되었습니다.

### 1.1 핵심 원칙

> **"Claude와의 효과적인 협업은 잘 구조화된 컨텍스트에서 시작된다."**

1. **컨텍스트 우선**: Claude에게 충분하고 명확한 컨텍스트 제공
2. **일관성 유지**: 코딩/문서 스타일 표준화
3. **모듈화**: 반복 사용되는 지침을 파일로 분리
4. **역할 명확화**: 문서별, 작업별 역할 정의
5. **점진적 자동화**: 자주 쓰는 작업부터 권한 승인

---

## 2. 프로젝트 구조

### 2.1 권장 디렉토리 구조

```text
your-project/
├── app.py (또는 main.py)    # 메인 애플리케이션
├── src/                     # 소스 코드
├── tests/                   # 테스트 코드
├── requirements.txt         # 의존성
├── .env.example            # 환경 변수 템플릿
├── .gitignore              # Git 제외 파일
│
├── README.md               # 사용자 가이드 (Level 1)
├── PRD.md                  # 제품 요구사항 (Level 2)
├── CLAUDE.md               # Claude 작업 가이드 (Level 3) ⭐ 필수
│
├── .claude/                # Claude 설정 폴더 ⭐ 필수
│   ├── settings.local.json # 로컬 권한 설정
│   └── commands/           # 커스텀 명령어
│       ├── commit-and-push.md
│       └── [task-name].md
│
├── prompts/                # 프롬프트 템플릿 ⭐ 권장
│   ├── [document]-instruction.md
│   └── [task]-template.md
│
└── documents/              # 산출물 문서
```

### 2.2 필수 파일 설명

| 파일/폴더 | 필수 여부 | 용도 |
| --------- | --------- | ---- |
| CLAUDE.md | **필수** | Claude에게 프로젝트 컨텍스트 제공 |
| .claude/ | **필수** | Claude 설정 및 커스텀 명령어 |
| prompts/ | 권장 | 재사용 가능한 프롬프트 템플릿 |
| PRD.md | 권장 | 제품 요구사항 정의 |
| README.md | 권장 | 사용자 가이드 |

---

## 3. CLAUDE.md 작성 가이드

CLAUDE.md는 **프로젝트의 전역 컨텍스트**를 제공하는 핵심 문서입니다.

### 3.1 필수 섹션

```markdown
# Claude AI 작업 가이드

## 프로젝트 개요
- 프로젝트 이름, 목적, 주요 기능

## 기술 스택
- 사용 중인 언어, 프레임워크, 라이브러리

## 프로젝트 구조
- 디렉토리 및 주요 파일 설명

## 코딩 컨벤션
- 네이밍 규칙, 스타일 가이드
- 코드 예시 포함

## 개발 환경 설정
- 설치 및 실행 방법

## Claude와의 협업 팁
- 효과적인 요청 방법
- 자주 사용하는 명령어
```

### 3.2 권장 섹션

```markdown
## 개발 가이드라인
- 파일 수정 시 주의사항
- 에러 핸들링 패턴

## 문서 작성 가이드라인
- 문서 역할 구분
- 문서 스타일 규칙

## 문제 해결 가이드
- 자주 발생하는 이슈와 해결 방법

## 배포 체크리스트
- 배포 전 확인 사항

## 향후 개발 방향
- 로드맵, Phase 별 계획
```

### 3.3 작성 팁

1. **구체적인 예시 포함**: 코드 예시, 명령어 예시 등
2. **좋은 예/나쁜 예 제시**: Claude가 판단 기준을 가질 수 있도록
3. **체크리스트 활용**: 빠뜨리기 쉬운 항목들을 리스트로
4. **마지막 업데이트 표시**: 문서의 최신성 확인

---

## 4. .claude 폴더 설정

### 4.1 settings.local.json

자주 사용하는 명령어를 사전 승인하여 워크플로우를 가속화합니다.

```json
{
  "permissions": {
    "allow": [
      "Bash(pip install:*)",
      "Bash(pip3 install:*)",
      "Bash(npm install:*)",
      "Bash(git init:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git branch:*)",
      "Bash(python3:*)",
      "Bash(npm run:*)",
      "Bash(source:*)"
    ]
  }
}
```

#### 권한 설정 원칙

1. **최소 권한 원칙**: 필요한 명령어만 승인
2. **안전 우선**: 위험한 명령어(rm -rf, force push 등)는 제외
3. **점진적 확장**: 필요할 때마다 추가

#### 자주 사용하는 권한 패턴

```json
// Git 관련
"Bash(git add:*)",
"Bash(git commit:*)",
"Bash(git push:*)",
"Bash(git pull:*)",
"Bash(git branch:*)",
"Bash(git checkout:*)",

// Python 관련
"Bash(pip install:*)",
"Bash(pip3 install:*)",
"Bash(python3:*)",
"Bash(pytest:*)",

// Node.js 관련
"Bash(npm install:*)",
"Bash(npm run:*)",
"Bash(yarn:*)",

// 기타
"Bash(source:*)",
"Bash(docker:*)"
```

### 4.2 commands/ 폴더

재사용 가능한 프롬프트 템플릿을 저장합니다.

#### 커스텀 명령어 작성법

**파일명**: `[command-name].md`

**구조**:

```markdown
# [명령어 제목]

[역할 부여]
너는 이제부터 [역할]이야. [구체적인 작업 설명].

## 작업 지침

1. [단계 1]
2. [단계 2]
3. [단계 3]

## 출력 형식

<output_template>
[출력 템플릿]
</output_template>

## 주의사항

- [주의사항 1]
- [주의사항 2]
```

#### 유용한 커스텀 명령어 예시

**commit-and-push.md**:

```markdown
# Git 커밋 및 푸시

너는 Git 커밋 전문가야. 현재 변경사항을 분석하고 커밋해줘.

## 커밋 메시지 형식

<commit_template>
[type]: [한줄 요약]

- [변경사항 세부 내용]

Co-Authored-By: Claude <noreply@anthropic.com>
</commit_template>

## 타입 종류

- feat: 새로운 기능
- fix: 버그 수정
- docs: 문서 수정
- refactor: 리팩토링
- test: 테스트
- chore: 기타
```

**code-review.md**:

```markdown
# 코드 리뷰

너는 시니어 개발자야. 코드를 리뷰하고 개선점을 제안해줘.

## 리뷰 항목

1. 코드 품질 (가독성, 유지보수성)
2. 성능 이슈
3. 보안 취약점
4. 에러 핸들링
5. 테스트 커버리지

## 출력 형식

### 요약
[전체 리뷰 요약]

### 개선 필요 (Critical)
- [심각한 이슈]

### 권장 사항 (Suggestion)
- [개선 제안]

### 잘한 점 (Good)
- [칭찬할 부분]
```

---

## 5. prompts 폴더 활용

### 5.1 용도

- 문서 작성 지침 (PRD, README 등)
- 반복 작업 템플릿
- 복잡한 프롬프트 분리

### 5.2 활용 방법

```markdown
<!-- 대화에서 참조 -->
@prompts/PRD-instruction.md 파일에 적힌 내용을 기반으로 PRD.md를 수정해줘.
```

### 5.3 예시: PRD-instruction.md

```markdown
# PRD 작성 지침

이 파일은 PRD를 작성하기 위한 참고 내용입니다.

## 문제 정의

[프로젝트가 해결하려는 문제 정의]

## 타겟 사용자

[핵심 사용자 정의]

## 문서 포맷

<문서포맷>
# [문서 제목]

- 작성자: [작성자]
- 버전: [버전]
- 최초 작성일: [날짜]

## 1. 개요 (Overview)

## 2. 문제 정의 (Problem Definition)

## 3. 타겟 사용자 (Target User)

...
</문서포맷>
```

---

## 6. 문서 체계

### 6.1 3계층 문서 구조

| 문서 | 대상 | 목적 | 톤 | 업데이트 시점 |
| ---- | ---- | ---- | -- | ------------- |
| README.md | 사용자 | 설치, 사용법 | 친근함 | 사용자 가이드 변경 시 |
| PRD.md | PM/기획자 | 제품 요구사항 | 공식적 | 제품 기능 변경 시 |
| CLAUDE.md | Claude/개발자 | 개발 가이드 | 실용적 | 개발 프로세스 변경 시 |

### 6.2 정보 분배 원칙

| 정보 | 마스터 문서 | 다른 문서 |
| ---- | ----------- | --------- |
| 프로젝트 구조 | 모두 동일 | - |
| 기술 스택 | PRD.md (상세) | README.md (간략) |
| 향후 계획 | PRD.md | README.md (요약) |
| 설치 방법 | README.md | - |
| 코딩 컨벤션 | CLAUDE.md | - |

### 6.3 문서 동기화 체크리스트

프로젝트 구조 변경 시:

- [ ] README.md 업데이트
- [ ] PRD.md 업데이트
- [ ] CLAUDE.md 업데이트
- [ ] 세 문서 일치 확인

---

## 7. Claude 협업 패턴

### 7.1 효과적인 요청 방법

#### 구체적으로 요청하기

```text
❌ 나쁜 예: "번역 기능 개선해줘"
✅ 좋은 예: "app.py의 translate 함수에 복사 버튼을 추가해줘"
```

#### 파일 경로 명시하기

```text
❌ 나쁜 예: "코드 수정해줘"
✅ 좋은 예: "src/utils/translator.py의 format_output 함수를 수정해줘"
```

#### 참조 파일 활용하기

```text
✅ 좋은 예: "@prompts/PRD-instruction.md 파일에 적힌 내용을 기반으로 PRD.md를 수정해줘"
```

#### 역할 부여하기

```text
✅ 좋은 예: "너는 이제부터 소프트웨어 개발 PM이야. PRD를 작성해줘."
```

### 7.2 컨텍스트 계층화

```text
Level 1: CLAUDE.md (전역 컨텍스트)
    ↓ Claude가 항상 참조
Level 2: .claude/commands/ (작업별 컨텍스트)
    ↓ 특정 명령어 실행 시 참조
Level 3: prompts/ (상세 지침 컨텍스트)
    ↓ @로 참조할 때 적용
Level 4: 대화 중 요청 (즉시 컨텍스트)
```

### 7.3 반복 작업 자동화

1. 자주 사용하는 명령어 → `.claude/settings.local.json`에 권한 추가
2. 자주 사용하는 프롬프트 → `.claude/commands/`에 파일 생성
3. 자주 사용하는 지침 → `prompts/`에 파일 생성

---

## 8. 워크플로우

### 8.1 신규 프로젝트 시작

```bash
# 1. 프로젝트 디렉토리 생성
mkdir my-project && cd my-project

# 2. Git 초기화
git init

# 3. 필수 파일 생성
touch CLAUDE.md
mkdir -p .claude/commands
touch .claude/settings.local.json
mkdir prompts

# 4. CLAUDE.md 작성 요청
# "이 프로젝트의 CLAUDE.md 초안을 만들어줘.
#  프로젝트는 [설명]이고, 기술 스택은 [스택]이야."
```

### 8.2 기능 개발 프로세스

```text
1. PRD.md에서 요구사항 확인
2. CLAUDE.md의 코딩 컨벤션 확인
3. 기능 구현
4. 테스트
5. 문서 업데이트 (필요시)
6. Git 커밋 (commit-and-push 명령어 활용)
```

### 8.3 문서 업데이트 프로세스

```text
1. 변경 범위 파악
2. 마스터 문서 먼저 업데이트
3. 관련 문서 동기화
4. markdownlint 규칙 확인
5. Git 커밋
```

---

## 9. 베스트 프랙티스

### 9.1 Do's

- CLAUDE.md를 최신 상태로 유지하기
- 코딩 컨벤션에 구체적인 예시 포함하기
- 커스텀 명령어로 반복 작업 자동화하기
- 문서 간 정보 일관성 유지하기
- 점진적으로 권한 추가하기

### 9.2 Don'ts

- CLAUDE.md 없이 프로젝트 시작하기
- 모든 명령어에 권한 부여하기 (보안 위험)
- 문서 간 정보 중복하기
- 모호한 요청 보내기
- 프로젝트 구조 변경 후 문서 미업데이트

---

## 10. 체크리스트

### 10.1 프로젝트 초기 설정

- [ ] CLAUDE.md 생성 및 작성
- [ ] .claude/ 폴더 생성
- [ ] settings.local.json 설정
- [ ] 기본 commands/ 생성 (commit-and-push 등)
- [ ] prompts/ 폴더 생성 (필요시)

### 10.2 CLAUDE.md 품질 확인

- [ ] 프로젝트 개요 포함
- [ ] 기술 스택 명시
- [ ] 프로젝트 구조 포함
- [ ] 코딩 컨벤션 정의 (예시 포함)
- [ ] 개발 환경 설정 방법
- [ ] Claude 협업 팁 포함

### 10.3 지속적 유지보수

- [ ] 프로젝트 구조 변경 시 문서 동기화
- [ ] 새 기능 추가 시 관련 문서 업데이트
- [ ] 정기적으로 CLAUDE.md 리뷰
- [ ] 유용한 커스텀 명령어 추가

---

## 11. 참고 자료

### 11.1 관련 문서

- [claude-development-guide-cot.md](./claude-development-guide-cot.md) - 이 가이드라인의 사고 과정

### 11.2 외부 리소스

- [Claude Code 공식 문서](https://docs.anthropic.com/claude-code)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)

---

**최종 수정일**: 2026년 1월 25일
