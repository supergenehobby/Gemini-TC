---
name: test-case-architect
description: |
  게임 Reference 문서를 분석하여 기존 테스트 케이스 패턴을 기반으로
  신규 게임 테스트 케이스를 자동 생성하는 QA 설계 스킬입니다.
  
  .gemini/TC-reference/ 폴더의 .textClipping 패턴 데이터를 기반으로
  .omc/reference/의 신규 게임 기획서 세션 파일에 일관되게 적용합니다.

  게임 테스트 케이스 자동 생성, 테스트 커버리지 작성이 필요할 때 사용하세요.
pattern_source: .gemini/TC-reference/
pattern_type: textClipping
input_source: .omc/reference/
output: .omc/testcase/{game_name}/
authoring_style: legacy-tc-pattern
---

# 🧪 Test Case Architect (TCA)

## 🎯 목적

기존 테스트 케이스 패턴을 기반으로 신규 게임의 Reference 세션 파일을 분석하여 일관된 형식의 테스트 케이스를 자동 생성한다.

이 스킬은 다음 두 가지 데이터를 결합하여 테스트 케이스를 생성한다:

1. 테스트 케이스 패턴 (Legacy Pattern)
2. 신규 게임 Reference 세션 파일 (Game Reference by Section)

---

# 📁 참조 경로

## 1. 테스트 케이스 패턴 (Legacy Pattern)

### 경로
`.gemini/TC-reference/`

이 폴더에는 기존 테스트 케이스 PDF를 분석하여 생성된 `.textClipping` 파일이 포함되어 있으며, **deep-interview 스킬**을 통해 생성된 테스트 케이스 패턴 데이터이다.

### 포함 정보:
- 테스트 케이스 컬럼 구조
- 컬럼 순서
- Step 작성 방식
- Expected Result 작성 방식
- 테이블 내 행 물리적 분리 규칙
- 테스트 케이스 분류 구조

⚠️ 패턴은 새로 생성하지 않는다. 반드시 `.textClipping`의 구조를 그대로 따른다.

---

## 2. 신규 게임 Reference 세션 파일 (Game Reference by Section)

### 경로
`.omc/reference/[게임명]/`

이 폴더에는 `deep-interview 스킬의 Phase 5 (Reference Generation)`을 통해 생성된 게임 기획서 **세션별 MD 파일**이 포함되어 있다.

### 세션 파일 구조
```
.omc/reference/[game_name]/
├─ [game_name]-index.md (Table of Contents)
│  (섹션 목록, 페이지 범위, 요약)
│
├─ 01_section_name.md (Pages XX–XX)
│  (섹션 1의 상세 내용)
│
├─ 02_section_name.md (Pages XX–XX)
│  (섹션 2의 상세 내용)
│
├─ 03_section_name.md (Pages XX–XX)
│  (섹션 3의 상세 내용)
│
└─ ... (모든 섹션의 파일)
```

**각 세션 파일의 구성:**
```markdown
# [Section Name] (Pages XX–XX)

## Overview
- 섹션 개요
- 주요 기능 설명

## Features
### Feature 1: [Feature Name]
- 설명
- 스펙
- UI/UX 상세사항
- 엣지 케이스

### Feature 2: [Feature Name]
- ...

## System Rules
- Rule 1: 동작 규칙
- Rule 2: 제약 조건
- ...

## Data Flow
- 입출력 스펙
- 상태 전이
- 데이터 일관성 규칙

## Exception Handling
- 에러 시나리오
- 복구 메커니즘
- 사용자 메시지
```

---

# 🔄 실행 프로세스

## Phase 1 — Pattern Loading

`.gemini/TC-reference/` 폴더의 모든 `.textClipping` 패턴 파일을 **반드시 읽고 로드**한다.

**필수 작업:**
1. `.textClipping` 파일 내용을 **완전히 읽는다.**
2. 파일에 포함된 **정확한 테이블 컬럼 구조를 추출**한다.
3. 추출한 컬럼 구조를 **이후 모든 TC 생성에 그대로 적용**한다.

**필수 컬럼 구조 (`.textClipping`에서 추출 필수):**
```
┌───────┬──────────┬──────────┬──────────┬────┬─────────────┬──────────────┐
│ 대분류 │ 중분류   │ 소분류   │ 사전조건 │ no │ 세부 스텝   │ 기대 결과    │
├───────┼──────────┼──────────┼──────────┼────┼─────────────┼──────────────┤
```

**각 컬럼의 정의:**
- **대분류**: 시스템 카테고리 (예: 시스템, 로비, 컨텐츠, 메타)
- **중분류**: 기능 그룹 (예: 진입, 기본 룰, 베팅, 스트릭)
- **소분류**: 세부 기능 또는 상세 항목 (예: UI/연출, 카드 제거, 배율 적용)
- **사전조건**: 테스트 시작 전 필요한 게임 상태 (예: 로비 진입, 인게임 진입, 레벨 시작 팝업)
- **no**: TC 고유 번호 (1, 2, 3, ...)
- **세부 스텝**: 사용자가 수행하는 단계별 액션 (1번, 2번, 3번, ... 각각 별도 행)
- **기대 결과**: 각 Step에 대응하는 기대 결과 (1번, 2번, 3번, ... 각각 별도 행)

**목적:**
- 테스트 케이스 컬럼 구조를 **정확히** 파악
- Step 작성 스타일을 **정확히** 파악
- Expected Result 작성 스타일을 **정확히** 파악

**⚠️ 절대 준수 사항:**
- ❌ 새로운 컬럼을 자의적으로 추가하지 않는다.
- ❌ 컬럼 순서를 변경하지 않는다.
- ❌ 컬럼 이름을 바꾸지 않는다.
- ❌ "ID", "테스트 항목", "테스트 시나리오" 같은 다른 컬럼을 사용하지 않는다.
- ✅ `.textClipping` 파일의 구조를 **100% 정확하게 따른다.**
- ✅ 의심스럽면 **파일을 다시 읽고 확인**한다.

---

## Phase 2 — Target Project Identification

사용자가 명령 시 전달한 게임명을 기준으로 Reference **세션 파일들**을 로드한다.

**예:** `.omc/reference/[Solitaire]/`

**세션 파일 구조:**
```
.omc/reference/[Solitaire]/
├─ [PST] Solitaire Tripeaks (2)-index.md
│  (인덱스: 섹션 목록, 페이지 범위, Summary)
│
├─ 개요.md (Pages 4–20)
│  (Deep Interview Phase 5에서 생성)
│
├─ 로비.md (Pages 21–26)
│  (Deep Interview Phase 5에서 생성)
│
├─ 로비팝업.md (Pages 27–40)
│  (Deep Interview Phase 5에서 생성)
│
├─ 인게임.md (Pages 41–54)
│  (Deep Interview Phase 5에서 생성)
│
├─ 기타팝업.md (Pages 55–59)
├─ 컨텐츠.md (Pages 60–64)
├─ 시스템.md (Pages 65–76)
├─ 컨텍스트전환.md (Pages 77–79)
├─ 튜토리얼.md (Pages 80–83)
├─ 소셜.md (Pages 84–91)
├─ 수익화.md (Pages 92–96)
├─ 기타.md (Pages 97–101)
├─ 마일스톤.md (Pages 102)
└─ 부록.md (Pages 104–108)
```

**처리 방식:**
- 인덱스 파일에서 섹션 목록과 대응하는 파일명을 파싱한다.
- 각 섹션에 대응하는 **세션 MD 파일을 순차적으로 로드**한다.
- 세션 파일의 **상세 내용**을 분석하여 구체적인 Feature와 Specification을 추출한다.

---

## Phase 3 — Reference Analysis

로드된 각 세션 파일을 순차적으로 분석한다.

**수행 작업:**

```python
# Step 1: 인덱스 파일에서 섹션 정보 파싱
index = load_file('[게임명]-index.md')
sections = parse_index_table(index)
# → [
#     {'no': '01', 'name': '개요', 'pages': '4–20', 'file': '개요.md'},
#     {'no': '02', 'name': '로비', 'pages': '21–26', 'file': '로비.md'},
#     ...
#   ]

# Step 2: 각 섹션별 세션 파일 로드 및 상세 분석
for section in sections:
    session_file = load_file(section['file'])
    
    # Step 3: 세션 파일에서 상세 내용 추출
    features = extract_features_from_file(session_file)
    # - Feature 이름: "카드 제거 규칙", "스트릭 미터", "베팅 시스템" 등
    # - Feature의 상세 설명: "Overview" 섹션에서 추출
    # - 구체적인 동작: "Features" 섹션에서 추출
    # - 시스템 규칙: "System Rules" 섹션에서 추출
    # - 데이터 흐름: "Data Flow" 섹션에서 추출
    # - 예외 상황: "Exception Handling" 섹션에서 추출
    
    # Step 4: 각 Feature별 Test Case 시나리오 계획
    for feature in features:
        # 다음을 기반으로 TC 시나리오 결정:
        # - Feature의 정상 동작
        # - 예외 상황 (Exception Handling에서 추출)
        # - UI 상태 변화 (Overview에서 추출)
        # - 데이터 상태 변화 (Data Flow에서 추출)
        # - 경계 조건 (System Rules에서 추출)
        test_scenarios = plan_test_scenarios(feature)
```

**Feature 유형 및 추출:**
- **UI 기능** (예: 로비 UI, 팝업 레이아웃)
  - 추출 위치: Overview, Features 섹션
  - 상세 정보: UI 요소, 상태 변화, 시각적 피드백

- **게임 로직** (예: 카드 제거 규칙, 스트릭 미터)
  - 추출 위치: Features, System Rules 섹션
  - 상세 정보: 로직 설명, 규칙, 계산 방식

- **상태 변화** (예: 난이도 변화, 게임 결과)
  - 추출 위치: Data Flow, Features 섹션
  - 상세 정보: 상태 전이, 트리거 조건

- **재화 처리** (예: 골드 획득, 해머 소모)
  - 추출 위치: System Rules, Data Flow 섹션
  - 상세 정보: 획득/소모 조건, 수량, 제약

- **예외/에러 처리** (예: 네트워크 실패, 유효하지 않은 입력)
  - 추출 위치: Exception Handling 섹션
  - 상세 정보: 에러 시나리오, 복구 방법

---

## Phase 4 — Test Case Generation

각 Feature에 대해 테스트 케이스를 생성한다.

### 📋 테이블 생성 알고리즘

**입력 데이터:**
```
섹션명, Feature명, Feature 상세정보, steps_list, results_list
↓
대분류(섹션명), 중분류(Feature명), 소분류(자동 결정), 사전조건(자동 결정), no, steps_list, results_list
```

**처리 로직:**

```python
# Step 1: 섹션 정보로부터 대분류, 중분류 결정
section = '개요'  # Phase 3에서 추출
feature = '게임 플로우'  # Phase 3에서 추출
feature_spec = feature['specification']  # Phase 3에서 추출한 상세사항

# Step 2: Feature 기반 소분류, 사전조건 결정 (자동)
소분류 = determine_subclass(feature, feature_spec)
# 예: "UI/플로우", "로직", "상태", "데이터", "예외처리"

사전조건 = determine_precondition(section, feature)
# 예: "앱 실행", "로비 진입", "게임 진행 중"

# Step 3: Feature 상세정보 기반 Test Case 시나리오 생성
scenarios = generate_test_scenarios(feature_spec)
# scenarios = [
#     {'type': 'normal', 'name': '정상 동작', 'steps': [...], 'results': [...]},
#     {'type': 'exception', 'name': '예외 상황', 'steps': [...], 'results': [...]},
#     {'type': 'state', 'name': 'UI 상태 변화', 'steps': [...], 'results': [...]},
#     ...
# ]

# Step 4: 각 시나리오별로 번호별 Step과 Result 파싱
for scenario in scenarios:
    steps = parse_numbered_items(scenario['steps'])
    results = parse_numbered_items(scenario['results'])
    num_rows = max(len(steps), len(results))
    
    # Step 5: 마크다운 테이블 생성 (Phase 1에서 추출한 정확한 컬럼 구조 사용)
    for i in range(num_rows):
        if i == 0:
            print(f"│ {대분류} │ {중분류} │ {소분류} │ {사전조건} │ {no} │ {steps[0]} │ {results[0]} │")
        else:
            print(f"├───┼────────┼────────┼────────┼────┼─────────────────┼─────────────────┤")
            print(f"│   │        │        │        │ {no} │ {steps[i]} │ {results[i]} │")
```

**출력 예시:**

```
┌───────┬──────────┬────────┬──────────┬────┬──────────────────────────┬──────────────────────────┐
│ 대분류 │ 중분류   │ 소분류 │ 사전조건 │ no │ 세부 스텝              │ 기대 결과                │
├───────┼──────────┼────────┼──────────┼────┼──────────────────────────┼──────────────────────────┤
│ 실행   │ 스플래시 │ UI/연출│ 앱 최초  │ 1  │ 1. 앱 아이콘을 터치한다 │ 1. 스플래시 화면이 노출됨│
│       │          │        │ 실행     │    │                          │                          │
├───────┼──────────┼────────┼──────────┼────┼──────────────────────────┼──────────────────────────┤
│       │          │        │          │ 1  │ 2. 로딩바 진행을 확인한다│ 2. 로딩바가 진행됨      │
├───────┼──────────┼────────┼──────────┼────┼──────────────────────────┼──────────────────────────┤
│       │          │        │          │ 1  │ 3. 로딩 완료를 대기한다  │ 3. 로비 화면으로 이동   │
└───────┴──────────┴────────┴──────────┴────┴──────────────────────────┴──────────────────────────┘
```

**규칙:**
- ✅ Phase 1에서 추출한 정확한 컬럼 구조 사용
- ✅ 입력에서 "1. ... 2. ... 3. ..." 형태 감지
- ✅ 숫자 기준으로 자동 분리
- ✅ 분리된 항목마다 **물리적 행(Row) 추가**
- ✅ `<br>` 태그 자동 제거
- ✅ 행과 행 사이에 마크다운 구분선(├─┼─┤) 자동 삽입

**Coverage 범위:**
각 Feature는 최소 다음 항목을 포함해야 한다:
- 정상 동작
- 예외 상황
- UI 상태 변화
- 데이터 상태 변화
- 경계 조건

**생성 수량:** 각 Feature당 최소 3개 이상의 테스트 케이스를 생성한다.

---

## Phase 5 — Reference Iteration

`.omc/reference/[게임명]/` 폴더의 모든 세션 파일을 순차적으로 처리한다.

**반복 규칙:**

```python
for section in sections:  # 인덱스의 모든 섹션 반복
    session_file = load_file(section['file'])
    features = extract_features_from_file(session_file)
    
    for feature in features:  # 각 섹션의 모든 Feature
        scenarios = generate_test_scenarios(feature)
        
        for scenario in scenarios:  # 각 Feature의 모든 시나리오
            test_cases = generate_test_cases(section, feature, scenario)
            save_to_output(test_cases)
```

생성 가능한 테스트 케이스 수에는 제한이 없다.

모든 Reference 섹션 처리가 완료되면 Phase 6 (Coverage Validation)을 수행한다.

---

## Phase 6 — Coverage Validation

생성된 테스트 케이스가 모든 세션 파일의 모든 Feature를 커버하는지 검사한다.

**수행 작업:**
1. Phase 3에서 추출한 모든 Feature 목록을 기준으로 Coverage를 확인한다.
2. 각 Feature가 최소 1개 이상의 테스트 케이스에 매핑되어 있는지 확인한다.
3. 각 Feature의 예외/에러 케이스가 TC로 작성되었는지 확인한다.
4. 테스트 케이스가 존재하지 않는 Feature가 발견될 경우 추가 TC를 생성한다.

**Coverage 규칙:**
- 모든 Feature는 최소 1개 이상의 TC를 가져야 한다.
- 핵심 게임 로직 Feature는 최소 3개 이상의 TC를 권장한다 (정상 + 예외 + 경계).
- UI Feature는 상태 변화 검증 TC를 포함해야 한다.
- Exception Handling에 정의된 모든 에러는 TC로 작성되어야 한다.

⚠️ 누락된 Feature가 존재할 경우 Phase 4 (Test Case Generation)를 재실행하여 보완한다.

---

# 🚀 트리거 명령어

**명시적 명령어:**
- `omc: generate-tc [게임명]`
- `omc: write-testcase [게임명]`

**자연어 요청:**
- `[게임명] 테스트 케이스 작성해줘`

---

# 📊 워크플로우 통합

```
PDF 입력
  ↓
omc: deep-interview [game_name] --auto-generate-reference
  ↓
Deep Interview Protocol
  Phase 1-4: 분석 + FRD 생성
  Phase 5: Reference MD 파일 자동 생성 ✅
  ↓
.omc/reference/[game_name]/
  ├─ index.md
  ├─ 개요.md
  ├─ 로비.md
  └─ ... (14개 파일)
  ↓
omc: generate-tc [game_name]
  ↓
Test Case Architect
  Phase 1: TC 패턴 로드
  Phase 2: 세션 파일 로드 ✅ (수정됨)
  Phase 3: 세션 파일 상세 분석 ✅ (수정됨)
  Phase 4: TC 생성
  Phase 5: 반복 처리
  Phase 6: Coverage 검증
  ↓
.omc/testcase/[game_name]/
  └─ 디테일한 테스트 케이스 자동 생성 ✅
```
