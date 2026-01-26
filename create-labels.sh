#!/bin/bash

# GitHub 레이블 생성 스크립트

echo "Creating GitHub labels..."

# 개발 영역 (Area)
echo "Creating area labels..."
gh label create "area: frontend" --description "프론트엔드 관련 작업" --color "0052CC" --force
gh label create "area: backend" --description "백엔드 관련 작업" --color "5319E7" --force
gh label create "area: ui/ux" --description "UI/UX 디자인 관련 작업" --color "1D76DB" --force
gh label create "area: database" --description "데이터베이스 관련 작업" --color "C5DEF5" --force
gh label create "area: infrastructure" --description "인프라 및 배포 관련 작업" --color "006B75" --force

# 복잡도 (Complexity)
echo "Creating complexity labels..."
gh label create "complexity: easy" --description "쉬운 작업 (1-2시간)" --color "0E8A16" --force
gh label create "complexity: medium" --description "보통 난이도 (2-4시간)" --color "FBCA04" --force
gh label create "complexity: hard" --description "복잡한 작업 (4시간 이상)" --color "D93F0B" --force

# 작업 유형 (Type)
echo "Creating type labels..."
gh label create "type: feature" --description "새로운 기능 추가" --color "0075CA" --force
gh label create "type: bug" --description "버그 수정" --color "D73A4A" --force
gh label create "type: documentation" --description "문서화 작업" --color "0075CA" --force
gh label create "type: test" --description "테스트 관련 작업" --color "BFD4F2" --force
gh label create "type: refactor" --description "코드 리팩토링" --color "FBCA04" --force
gh label create "type: enhancement" --description "기능 개선" --color "A2EEEF" --force

# 우선순위 (Priority) - 추가
echo "Creating priority labels..."
gh label create "priority: critical" --description "긴급 처리 필요" --color "B60205" --force
gh label create "priority: high" --description "높은 우선순위" --color "D93F0B" --force
gh label create "priority: medium" --description "보통 우선순위" --color "FBCA04" --force
gh label create "priority: low" --description "낮은 우선순위" --color "0E8A16" --force

# 상태 (Status) - 추가
echo "Creating status labels..."
gh label create "status: blocked" --description "블로킹 이슈로 작업 중단" --color "D93F0B" --force
gh label create "status: in-progress" --description "작업 진행 중" --color "1D76DB" --force
gh label create "status: review-needed" --description "리뷰 필요" --color "FBCA04" --force
gh label create "status: ready" --description "작업 준비 완료" --color "0E8A16" --force

echo "✅ All labels created successfully!"
