# GitHub 이슈 관리

TransBot 프로젝트의 GitHub 이슈 관리 가이드입니다.

## 레이블 생성 스크립트

이 프로젝트는 GitHub 이슈를 체계적으로 관리하기 위한 `create-labels.sh` 스크립트를 제공합니다.

### 사전 요구사항

- **GitHub CLI (`gh`)**: 설치 및 인증 필요
  - 설치: `brew install gh` (macOS) 또는 [GitHub CLI 공식 사이트](https://cli.github.com/)
  - 인증: `gh auth login`

### 스크립트 실행 방법

```bash
# 실행 권한 부여
chmod +x create-labels.sh

# 스크립트 실행
./create-labels.sh
```

## 생성되는 레이블 (총 21개)

### 1. Area (개발 영역) - 5개

- `area: frontend` - 프론트엔드 관련 작업 (파란색 #0052CC)
- `area: backend` - 백엔드 관련 작업 (보라색 #5319E7)
- `area: ui/ux` - UI/UX 디자인 관련 작업 (파란색 #1D76DB)
- `area: database` - 데이터베이스 관련 작업 (하늘색 #C5DEF5)
- `area: infrastructure` - 인프라 및 배포 관련 작업 (청록색 #006B75)

### 2. Complexity (복잡도) - 3개

- `complexity: easy` - 쉬운 작업, 1-2시간 (초록색 #0E8A16)
- `complexity: medium` - 보통 난이도, 2-4시간 (노란색 #FBCA04)
- `complexity: hard` - 복잡한 작업, 4시간 이상 (주황색 #D93F0B)

### 3. Type (작업 유형) - 6개

- `type: feature` - 새로운 기능 추가 (파란색 #0075CA)
- `type: bug` - 버그 수정 (빨간색 #D73A4A)
- `type: documentation` - 문서화 작업 (파란색 #0075CA)
- `type: test` - 테스트 관련 작업 (하늘색 #BFD4F2)
- `type: refactor` - 코드 리팩토링 (노란색 #FBCA04)
- `type: enhancement` - 기능 개선 (하늘색 #A2EEEF)

### 4. Priority (우선순위) - 4개

- `priority: critical` - 긴급 처리 필요 (진한 빨간색 #B60205)
- `priority: high` - 높은 우선순위 (주황색 #D93F0B)
- `priority: medium` - 보통 우선순위 (노란색 #FBCA04)
- `priority: low` - 낮은 우선순위 (초록색 #0E8A16)

### 5. Status (상태) - 4개

- `status: blocked` - 블로킹 이슈로 작업 중단 (주황색 #D93F0B)
- `status: in-progress` - 작업 진행 중 (파란색 #1D76DB)
- `status: review-needed` - 리뷰 필요 (노란색 #FBCA04)
- `status: ready` - 작업 준비 완료 (초록색 #0E8A16)

## 레이블 색상 코딩

- **빨간색 계열**: 긴급/중요 (critical, bug)
- **주황색 계열**: 높은 우선순위/복잡도 (high, hard, blocked)
- **노란색 계열**: 보통 수준 (medium)
- **초록색 계열**: 낮은 우선순위/쉬운 작업 (easy, low, ready)
- **파란색 계열**: 개발 영역 및 작업 유형
- **하늘색 계열**: 문서/테스트 관련

## 레이블 사용 예시

```bash
# 새로운 기능 이슈
Labels: type: feature, area: frontend, complexity: medium, priority: high

# 버그 수정 이슈
Labels: type: bug, area: backend, complexity: easy, priority: critical

# 문서 작업 이슈
Labels: type: documentation, complexity: easy, priority: low
```

## 레이블 커스터마이징

`create-labels.sh` 파일을 직접 수정하여 레이블을 커스터마이징할 수 있습니다:

```bash
# 새로운 레이블 추가
gh label create "area: api" --description "API 관련 작업" --color "0052CC" --force

# 기존 레이블 삭제
gh label delete "area: database"

# 레이블 이름 변경 (기존 삭제 후 재생성 필요)
gh label delete "complexity: easy"
gh label create "complexity: simple" --description "간단한 작업" --color "0E8A16" --force
```

## 레이블 관리 주의사항

- `--force` 플래그: 기존 레이블이 있으면 덮어씁니다
- 레이블 삭제 시 연결된 이슈의 레이블도 함께 제거됩니다
- 색상 코드는 # 없이 6자리 HEX 코드로 입력합니다

---

마지막 업데이트: 2026-01-31
