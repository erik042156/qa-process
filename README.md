# AI를 활용한 QA process

요구사항 분석 → Test Case 설계 → 자동화 대상 선정 → E2E 구현 → CI
결과 확인까지 이어지는 QA Automation Workflow를 구축한 프로젝트입니다.

단순히 AI를 이용해 결과물을 생성하는 것이 아니라, 반복적인 QA 작업은 AI가 보조하고
요구사항 해석, Test Coverage, 자동화 대상 선정 등 QA 판단이 필요한 단계에는 QA Engineer의
승인을 유지하는 구조를 목표로 설계했습니다.

전체 운영 원칙은 [`CLAUDE.md`](./CLAUDE.md)를 따릅니다.

대상 : 테스트 자동화 연습용 이커머스
사이트[Automation Exercise](https://automationexercise.com/)

---

1. Project Goal
2. Requirements
3. QA Workflow
4. AI / QA Engineer 역할
5. Automation Strategy
6. Test Coverage
7. Architecture
8. CI & Reporting
9. Challenges
10. Output
11. Project Structure
12. Installation / How to Run
13. Documents

---

## 1. Project Goal

### 목표

반복적인 QA 업무에 AI를 활용하되, 요구사항 분석이나 Test Case 최종 승인, 자동화 대상
선정 등 QA 판단이 필요한 단계는 사람이 직접 검토·승인하는 Workflow를 설계하는 것을
목표로 했습니다.

### 해결하고자 한 사항

- 요구사항 → TC → 자동화 코드 사이의 추적성 부족
- 반복적인 Test Case 및 자동화 코드 작성 비용
- 자동화 대상 선정 기준이 불명확해지는 문제
- AI가 생성한 결과를 검증 없이 사용하는 위험
- 테스트 실행 및 결과 확인의 반복 작업

### Contribution

- 요구사항 → TC → 자동화 대상 선정 → E2E → CI/Report로 이어지는 QA Workflow 설계
- 공개 서비스 분석을 기반으로 프로젝트용 Project/Feature PRD 작성 및 Test Case 검토·확정
- 자동화 대상 선정 기준(Automation Score 6개 축) 정의 및 최종 자동화 대상 결정
- Python/Selenium/pytest/POM 기반 E2E 자동화 구조 설계 및 구현
- GitHub Actions 기반 Regression 실행과 Slack 결과 알림 구조 구성
- Claude Code Sub Agent/Skill의 역할과 QA 승인 지점 설계([`CLAUDE.md`](./CLAUDE.md))

## 2. Requirements

Automation Exercise는 테스트 자동화 연습을 위해 공개된 이커머스 사이트로, 별도의 내부
기획서가 존재하지 않습니다. 따라서 공개된 범위 내에서 실제로 확인 가능한 기능과 동작을
근거로 프로젝트용 PRD를 별도로 작성했습니다. 이 프로젝트의 PRD는 실제 서비스 운영사의
내부 요구사항 문서가 아니라, **QA Workflow를 검증하기 위한 요구사항 입력값**으로
사용했습니다.

**현재 프로젝트 진행 방식**

```
서비스 기능 확인 → 프로젝트용 PRD 작성 → Test Case 생성 → QA 검토/승인 → 자동화 대상 선정 → E2E 자동화 구현
```

**실제 업무 적용 방향**

별도의 PRD를 임의로 생성하는 것이 아닌, 실제 기획서·정책서·요구사항 문서를 사용하는
것을 전제로 합니다.

```
기획서/정책서/요구사항 → Claude Code 기반 요구사항 분석 → Test Case 초안 생성
  → QA Engineer 검토 → Test Case 확정 → 자동화 대상 선정 → E2E 자동화 구현
```

요구사항에 정의되지 않은 정책이나 Expected Result는 AI가 임의로 결정하지 않고
QA Engineer 확인이 필요한 항목으로 분류해, 검토를 거친 뒤 TC에 반영하는 방향을
지향합니다. 실제로 signup-delete-account/top-navigation/product-search Feature에서
구현 중 실제 사이트 동작이 승인된 PRD/TC와 달라, 사용자 확인을 거쳐 PRD/TC를
재승인한 사례가 있습니다(자세한 내용은 [`docs/roadmap/ROADMAP.md`](./docs/roadmap/ROADMAP.md)
9절 참고).

## 3. QA Workflow

```
Requirements (PRD)
      ↓
TC Draft (Test Case 초안)
      ↓
QA Review / TC 확정
      ↓
자동화 대상 선정
      ↓
QA Decision (자동화 대상 선정 승인)
      ↓
Automation (E2E 구현)
      ↓
CI (GitHub Actions 실행 → Report → Slack)
```

각 화살표 이전 단계는 사람의 승인을 거쳐야 다음 단계로 넘어갑니다
(4절 AI / QA Engineer 역할, [`CLAUDE.md`](./CLAUDE.md) 18절 User Approval 원칙).
세부 흐름은 `CLAUDE.md` 3절을 따릅니다.

## 4. AI / QA Engineer 역할

AI는 QA Engineer의 판단을 대체하는 것이 아니라, 반복 작업을 줄이고 QA Engineer가 Risk와
품질 판단에 집중할 수 있도록 보조하는 역할로 사용합니다.

| QA 단계 | AI / Automation | QA Engineer |
|---|---|---|
| 요구사항 분석 | 문서 분석/구조화 | 요구사항 해석/누락 검토 |
| TC 설계 | TC 초안 생성 | TC 검토 및 최종 승인 |
| 정책 모호성 | 확인 필요 항목 식별 | 실제 사이트 확인/정책 확정 |
| 자동화 선정 | 후보 분석(Automation Score) | Risk/ROI 기반 최종 선정 |
| 구현 | 코드 생성 보조 | 구조/Assertion/Locator 검토 |
| 실행 | CI 자동 실행 | 실패 원인 분석 |
| 결과 | Report/Slack 전달 | 품질 판단 |

## 5. Automation Strategy

**자동화 우선순위**

- 핵심 사용자 Flow
- Regression 영향도가 높은 기능
- Expected Result가 명확한 TC
- 안정적으로 재현 가능한 TC

**Manual 유지**

- UI/UX의 주관적 판단이 필요한 영역
- Production 사이트의 알려진 결함으로 재현이 불안정한 영역
- 변경 빈도가 높아 유지보수 비용이 큰 영역(추정)

**세부 평가 기준**

- Automation Score 평가 기준 6개
  - Business Criticality
  - Regression Frequency
  - Automation Stability
  - Result Determinism
  - Manual Test Cost
  - Maintenance Cost

- 참고: [`automation-candidate` Skill](./.claude/skills/automation-candidate/)

- TC별 실제 평가 결과와 최종 QA Decision은
  [`docs/tc/automation-candidates/`](./docs/tc/automation-candidates/)에서 확인할 수
  있습니다.

## 6. Test Coverage

| Feature | TC | Automated | 주요 검증 |
|---|---|---|---|
| login-logout | 16 | 11 | 로그인/로그아웃, 세션 유지, 잘못된 계정 처리 |
| signup-delete-account | 16 | 11 | 회원가입, 계정 삭제, 입력값 검증 |
| top-navigation | 11 | 6 | 로그인 상태별 상단 메뉴 구성, 페이지 이동 |
| product-search | 10 | 8 | 검색 결과 매칭, 브랜드/카테고리 검색 |
| cart | 16 | 13 | 담기/삭제/빈 카트, 수량·합계 계산 |
| product-detail | 27 | 6 | 상품 정보, Add to cart 모달, 리뷰 |
| page-ui | 41 | 21 | 홈/상품 목록/카테고리·브랜드/체크아웃 UI 요소 |
| **합계** | **137** | **76** | |

- **TC**: `docs/tc/*.md`에 정의된, 자동화 대상 선정 이전 전체 Test Case 개수
- **Automated**: 사용자 승인을 거쳐 자동화 대상으로 확정되어 실제 구현된 E2E Test 개수
  (`automation/tests/*.py`, 일부 TC는 `pytest.mark.parametrize`로 확장되어 실제 실행
  케이스는 79건)
- 나머지(TC − Automated)는 "5. Automation Strategy"의 Manual 유지 기준 또는 외부
  요소(제3자 광고, 리뷰 등) 의존성 등의 사유로 Hold/Rejected 처리된 TC이며, TC별 사유는
  `docs/tc/automation-candidates/*.md`에서 확인할 수 있습니다.

## 7. Architecture

- **Language**: Python (자동화 코드 한정 PEP8 예외 — 4칸 들여쓰기, snake_case,
  [`CLAUDE.md`](./CLAUDE.md) 전역 규칙(2칸/camelCase)과 별개로 사용자 승인)
- **E2E Framework**: Selenium WebDriver
- **Test Runner**: pytest + pytest-html(HTML/JUnit XML 리포트)
- **설계 패턴**: Page Object Model — 화면 1개당 Page 객체 1개(`automation/pages/`),
  `BasePage`를 상속해 클릭/입력/대기 등 공통 로직과 광고 오버레이 방어 로직을 공유
- **AI 워크플로우**: Claude Code 기반 Sub Agent/Skill(`.claude/agents/`,
  `.claude/skills/`) — PRD 작성, TC 생성, 자동화 대상 선정, Roadmap 작성, 자동화 코드
  구현을 각각 단일 책임의 Agent/Skill로 분리해 역할이 서로 침범하지 않도록 구성
  ([`CLAUDE.md`](./CLAUDE.md) 6절)

## 8. CI & Reporting

```
Code Push
    ↓
GitHub Actions
    ↓
pytest (headless Chrome)
    ↓
E2E Test
    ↓
HTML / JUnit XML Report
    ↓
Artifact
    ↓
Slack Notification (실패 시에만)
```

**목적**
> - 반복적으로 수행하는 Regression 테스트를 자동화하고 정해진 시점에 CI에서 실행해
>   수동 수행 비용을 줄인다.
> - 매일 정해진 시각에 정기 실행해 결과를 주기적으로 확인할 수 있게 한다.

- **GitHub Actions**: `master` 브랜치 Push 시 자동 실행 + 매일 한국시간(KST) 오전
  9시 스케줄 실행 + 수동 실행(workflow_dispatch), `ubuntu-latest` / Python 3.9
  (`.github/workflows/ci.yml`)
- **Report**: 실행마다 pytest-html(`report.html`)/JUnit XML(`results.xml`)을
  생성합니다.
- **Artifact**: 리포트(`automation/reports/`)와 실패 스크린샷(`automation/screenshots/`)을
  GitHub Actions Artifact로 업로드해 사후 확인이 가능하도록 합니다.
- **Slack Notification**: 실패한 테스트가 있을 때만 실패 테스트 이름과 실패 코드
  위치(파일:라인)를 요약해 Slack Webhook으로 전달합니다(Commit/Push 승인 용도로는
  사용하지 않음, [`CLAUDE.md`](./CLAUDE.md) 16절). 스크립트는 표준 라이브러리만 사용해
  구현되어 있습니다(`scripts/notify_slack/notify.py`).

## 9. Challenges

### Challenge 1. 제3자 광고 오버레이로 인한 테스트 방해

- **문제**: Automation Exercise는 Production 단일 환경이며, 사이트 자체가 아닌 제3자
  광고 네트워크(Google Ads)가 페이지 진입 시 무작위로 전면 광고 오버레이(Google
  Vignette 등)를 주입해 실제 클릭/입력을 가로막는 현상이 확인되었습니다.
- **판단**: 광고 콘텐츠 자체는 PRD/TC의 검증 대상이 아니므로, 화면마다 개별적으로
  우회 로직을 넣기보다 공통 계층에서 한 번에 방어하는 것이 유지보수 측면에서
  적합하다고 판단했습니다.
- **해결**: `BasePage`에 `_dismiss_ad_overlay_if_present()` 공통 메서드를 추가해
  `click()`/`type_text()` 시작 시점에 자동으로 호출되도록 구성했습니다. 오버레이가
  있으면 닫고, 없으면 짧은 타임아웃 후 조용히 통과합니다. `BasePage`를 상속하기만
  하면 모든 Page Object가 별도 구현 없이 이 방어 로직을 적용받습니다.
- **결과**: 새 화면을 추가할 때마다 광고 방어 로직을 중복 구현할 필요가 없어졌고,
  광고 마크업이 바뀌더라도 `BasePage` 한 곳만 수정하면 되는 구조를 확보했습니다.
  (상세: [`AUTOMATION_GUIDE.md`](./docs/automation/AUTOMATION_GUIDE.md) 7.1절)

### Challenge 2. Production 사이트 자체의 간헐적 결함과 자동화 실패의 구분

- **문제**: `/logout` 직접 접근 테스트(`test_logout_via_direct_url`)가 간헐적으로
  실패했습니다. 로컬(headed)뿐 아니라 GitHub Actions(headless) 환경에서도 재현되었고,
  자동화 코드는 이 기간 동안 변경되지 않았습니다.
- **판단**: 코드 변경 없이 발생하는 간헐적 실패이므로, 자동화 코드/Locator/Assertion
  문제로 단정하지 않고 Production 사이트 자체의 문제 가능성을 먼저 조사했습니다.
- **해결**: 재현 시점의 스크린샷과 사이트 응답을 직접 확인한 결과, `/logout` 엔드포인트가
  세션에 `user_id` 키가 이미 없는 경우 예외 처리 없이 접근해 서버에서 HTTP 500(Django
  `KeyError`)을 반환하는 실제 서버 결함임을 확인했습니다.
- **결과**: 이 결함을 이유로 Assertion을 완화하거나 실패를 자동으로 우회 처리하지
  않고, "알려진 Production 사이트 결함"으로 별도 문서화했습니다([`CLAUDE.md`](./CLAUDE.md)
  13절의 "실제 Product 문제" 분류). 이후 동일 테스트가 실패하면 이 결함 여부를
  우선 검토하되, 매번 자동으로 PASS 처리하지 않고 증거를 재확인한 뒤 판단합니다.
  (상세: [`AUTOMATION_GUIDE.md`](./docs/automation/AUTOMATION_GUIDE.md) 22.1절)

### Challenge 3. CI 알림 조건의 논리 오류

- **문제**: GitHub Actions 워크플로우에서 pytest 실행 스텝에 `continue-on-error: true`를
  적용한 상태로 Slack 알림 스텝에 `if: failure()` 조건을 그대로 사용하면, 실패가
  job 결론에 즉시 반영되지 않아 알림 스텝이 **영원히 실행되지 않는** 논리 오류가
  됨을 구현 중 발견했습니다.
- **판단**: 알림이 아예 발송되지 않는 것은 CI 운영 목적(실패를 빠르게 인지)에 정면으로
  반하는 문제이므로, 배포 전에 반드시 실제 실행으로 검증이 필요하다고 판단했습니다.
- **해결**: `if: failure()` 대신 `if: steps.run_tests.outcome == 'failure'`로
  조건식을 수정해 `run_tests` 스텝의 개별 결과를 직접 참조하도록 변경했습니다.
- **결과**: 의도적으로 실패하는 테스트를 임시로 추가해 실제 GitHub Actions 실행에서
  Slack 알림이 정상 도착하는 것까지 검증한 뒤, 임시 테스트를 제거하고 `master`를
  원상 복구했습니다. (`.github/workflows/ci.yml`,
  [`docs/roadmap/ROADMAP.md`](./docs/roadmap/ROADMAP.md) 9절 Phase Final)

## 10. Output

- 요구사항 → TC → 자동화 구현으로 이어지는 Claude Code Agent/Skill 기반 QA Workflow 구축
- 전체 137개 TC 중 76개 TC를 E2E 자동화(실제 실행 케이스 79건)
- TC ↔ 자동화 코드 ↔ 테스트 결과 추적 구조 구성
- Selenium + pytest + POM 기반 자동화 Framework 구축
- GitHub Actions 기반 정기(Push + 매일 KST 09:00) Regression 실행
- HTML Report / 실패 Screenshot / Slack 결과 알림 구성

---

## 11. Project Structure

```
qa-process/
├── CLAUDE.md                       # 최상위 운영 원칙(Agent/Skill 공통 규칙)
├── docs/                           # PRD, TC, Roadmap, 자동화 가이드 (13. Documents 참고)
├── .claude/
│   ├── agents/                     # Sub Agent 정의(PRD/TC/자동화 대상 선정/Roadmap/구현)
│   └── skills/                     # Skill 정의(automation-candidate, tc-writing)
├── .github/workflows/ci.yml        # CI 워크플로우
├── scripts/
│   ├── notify_slack/               # CI 실패 시 Slack Webhook 알림 스크립트
│   └── sheets_sync/                # TC 작성 Agent용 Google Sheets 연동 모듈
└── automation/                     # 자동화 코드 (Selenium + pytest + POM)
    ├── conftest.py                 # WebDriver fixture(CI 환경 headless 분기), 실패 시 스크린샷 hook
    ├── pytest.ini, requirements.txt
    ├── config/                     # Base URL, 계정 등 환경 설정
    ├── pages/                      # Page Object (화면별 1클래스, BasePage 상속)
    ├── tests/                      # pytest 테스트 (Assertion 전담)
    ├── utils/                      # 화면과 무관한 공통 로직(계정 생성, 텍스트 정규화 등)
    ├── test_data/                  # 정적 테스트 데이터
    ├── reports/, screenshots/      # 실행 산출물 (git 미추적)
```

## 12. Installation / How to Run

### 사전 준비물

- Python 3.9
- Google Chrome — `selenium>=4.20.0`이 Selenium Manager로 버전에 맞는 chromedriver를
  자동 설치하므로 chromedriver를 별도로 설치할 필요는 없습니다.

### 설치 및 환경변수 설정

```bash
cd automation
pip install -r requirements.txt
cp .env.example .env
```

`.env`에 값을 채웁니다(`automation/.env.example` 참고, 파일은 `.gitignore`에 포함되어
커밋되지 않습니다):

| 변수 | 용도 |
|---|---|
| `ACTEST1_PASSWORD` / `ACTEST2_PASSWORD` / `ACTEST3_PASSWORD` | 사전 준비된 고정 테스트 계정 3개(`actest1~3@test.com`, 이메일은 `test_data/accounts.json`)의 비밀번호 |

### 실행

```bash
pytest tests/                                             # 전체 실행
pytest tests/test_login.py                                # 파일 단위 실행
pytest tests/test_cart.py::test_add_to_cart_shows_modal    # 단일 테스트 실행
pytest tests/ -k "search"                                  # 이름 패턴 매칭
```

로컬 실행은 기본적으로 headless가 아니라 Chrome 창이 실제로 뜹니다(`conftest.py`의
`driver` fixture가 `CI` 환경변수 유무로 headless 여부를 분기하며, CI에서만 headless를
적용합니다).

### 실행 결과 확인

`pytest.ini`의 `addopts`와 별개로 CI에서는 아래 리포트를 명시적으로 생성합니다(로컬에서도
동일한 옵션을 직접 붙이면 같은 파일이 생성됩니다).

```bash
pytest tests/ --html=reports/report.html --self-contained-html --junitxml=reports/results.xml
```

- HTML 리포트: `automation/reports/report.html`
- JUnit XML 리포트: `automation/reports/results.xml` (CI의 Slack 알림이 파싱하는 것과
  동일한 형식)
- 실패 시 자동 저장되는 스크린샷: `automation/screenshots/`

셋 다 `.gitignore`에 포함되어 커밋되지 않습니다.

### 문제가 생겼을 때

- 로그인 관련 에러가 나면 `.env` 값 누락·오타를 먼저 확인하세요.
- `test_logout_via_direct_url`이 간헐적으로만 실패하면
  [`AUTOMATION_GUIDE.md`](./docs/automation/AUTOMATION_GUIDE.md) 22.1절(알려진
  Production 사이트 결함)을 참고하세요.

## 13. Documents

| 구분 | 위치 | 비고 |
|---|---|---|
| Project PRD | `docs/prd/project-prd.md` | 서비스 개요, 대상 범위 |
| Feature PRD | `docs/prd/feature/*.md` | 로그인/회원가입/네비게이션/검색/카트/상품상세/UI |
| Test Case | `docs/tc/*.md` | Feature별 TC, Google Spreadsheet와 동기화 |
| 자동화 대상 선정 | `docs/tc/automation-candidates/*.md` | QA Decision(Approved/Hold/Rejected) 근거 |
| Roadmap | `docs/roadmap/ROADMAP.md` | Phase별 구현 순서 및 진행 현황, 승인됨 |
| 자동화 컨벤션 | `docs/automation/AUTOMATION_GUIDE.md` | Selenium/pytest 컨벤션, 발견된 이슈·해결 이력 |

각 문서는 상단에 상태(승인완료 등) 메타데이터와 하단 변경 이력을 가지며, 승인된 상위
문서는 후속 단계에서 임의로 수정하지 않습니다([`CLAUDE.md`](./CLAUDE.md) 7절).

`.claude/agents/`, `.claude/skills/`에는 PRD 작성·TC 작성·자동화 대상 선정·Roadmap
작성·자동화 코드 구현을 담당하는 전용 Agent/Skill이 정의되어 있으며, 각각 단일 책임만
가지고 서로의 역할을 침범하지 않습니다([`CLAUDE.md`](./CLAUDE.md) 6절).
