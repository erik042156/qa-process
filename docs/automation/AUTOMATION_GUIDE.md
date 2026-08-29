---
문서유형: Automation Guide
상태: 승인완료
참고: refer_CLAUDE.md(타 프로젝트 개발 규칙) 구조를 참고하되, 규칙 내용은 본 프로젝트에서
      사용자와 별도로 확정한 결정 사항을 따름
최초 작성일: 2026-08-27
최근 변경일: 2026-08-29
승인일: 2026-08-27
---

# AUTOMATION_GUIDE.md - QA Process 자동화 코드 개발 기준

## 0. 문서 목적 및 범위

이 문서는 `qa-process` 프로젝트의 **자동화 코드 개발 기준**을 정의하는 Source of Truth이며,
다음 작업에서 공통 판단 근거로 사용합니다.

- 자동화 개발 Roadmap 작성
- Shrimp Task 생성 및 작업 분해
- 자동화 코드 개발
- 코드 리뷰 및 테스트 실행/검증

이 문서는 **기능별 요구사항(로그인, 장바구니 등)을 다루지 않습니다.** 기능별 요구사항은
`docs/prd/feature/{slug}.md`(Feature PRD)와 `docs/tc/{slug}.md`(TC)를 Source of Truth로
합니다. 이 문서와 PRD/TC/Roadmap의 내용이 서로 다르게 보이면, 요구사항·시나리오 판단은 항상
PRD/TC를 기준으로 하고, **코드 작성 방식(구조/컨벤션/원칙)에 대한 판단만 이 문서를 기준으로**
합니다.

**아직 실제 코드, 디렉터리, 설정 파일은 생성되지 않았습니다.** 이 문서는 앞으로 자동화 코드를
작성할 때 따를 규칙을 정의하며, 이후 실제 구현 상태가 이 문서와 달라지면(CLAUDE.md 8절
"실제 구현 상태 = Repository Code" 원칙에 따라) 문서를 갱신합니다.

### 0.1 자동화 대상 범위

이 문서가 정의하는 규칙이 적용되는 자동화 대상은 다음 조건을 **모두** 만족하는 TC로 한정합니다
(`automation-candidate-agent`가 정의한 조건과 동일).

```
Candidate 문서(docs/tc/automation-candidates/{slug}.md) 상태 = 자동화대상확정
AND
QA Decision = Approved
```

2026-08-27 기준 대상 Feature와 Approved TC 건수는 다음과 같습니다(상세 TC 목록은 각
Candidate 문서를 Source of Truth로 참조하며, 이 문서에 전체 TC를 복제하지 않습니다).

| Feature | Approved TC 수 |
|---|---|
| cart | 13 |
| login-logout | 11 |
| page-ui | 21 |
| product-detail | 6 |
| product-search | 7 |
| signup-delete-account | 11 |
| top-navigation | 6 |

이 범위는 프로젝트마다 달라질 수 있으므로, 이 문서의 원칙 자체는 특정 Feature 목록에 종속되지
않고 재사용 가능하게 작성합니다.

---

## 1. Technology Stack

| 항목 | 결정 | 비고 |
|---|---|---|
| 언어 | **Python** | 1.1절 "코딩 스타일 예외" 적용 대상 |
| 자동화 도구 | **Selenium WebDriver** | |
| 테스트 러너 | **pytest** | |
| 설계 패턴 | **Page Object Model (POM)** | |
| 리포팅 | **pytest-html + JUnit XML(`--junitxml`) 병행** | HTML은 사람이 보는 Artifact, JUnit XML은 Slack 실패 메시지 조립용 |
| 실행 브라우저 | **Chrome (ChromeDriver)** | Project PRD 테스트 환경(Chrome) 기준 |
| 대상 환경 | Production 단일 환경 (`https://automationexercise.com/`) | 별도 dev/staging 없음(Project PRD 3절) |
| CI/CD | **GitHub Actions** | Push 시 자동 테스트 실행(16절) |
| 알림 | **Slack** | 실패 시 실패 원인 요약 포함 알림(CLAUDE.md 16절: 승인 용도 아님, 결과 알림 전용) |
| 패키지 버전 관리 | `requirements.txt` (미생성) | 실제 구현 시작 시 작성 |

### 1.1 코딩 스타일 예외 (중요)

프로젝트 전역 CLAUDE.md는 "들여쓰기 2칸, camelCase/PascalCase(컴포넌트)"를 기본 스타일로
정의하지만, **Python 자동화 코드에 한해 다음과 같이 PEP8을 우선 적용하는 예외를 사용자
승인(2026-08-27)으로 확정합니다.**

- 들여쓰기: **4칸** (2칸 아님)
- 변수/함수명: **snake_case** (camelCase 아님)
- 클래스명: PascalCase (전역 규칙과 동일, 충돌 없음)
- 상수(Locator 등): UPPER_SNAKE_CASE

이유: `black`/`flake8` 등 Python 표준 도구 체인이 4칸 들여쓰기와 PEP8 네이밍을 전제로 하고,
Selenium/표준 라이브러리 API 자체가 snake_case이므로 일관성을 위해 예외를 인정합니다. 이
예외는 **이 프로젝트의 Python 자동화 코드에만 적용**되며, PRD/TC/Roadmap 등 Markdown
문서나 다른 언어로 작성될 도구(`scripts/sheets_sync`의 기존 코드 포함)의 컨벤션까지 바꾸는
것은 아닙니다.

---

## 2. Automation Architecture

- **Page Object Model (POM)**을 채택합니다. 1개 웹 페이지(또는 명확히 구분되는 주요 화면
  영역)당 1개 Page 클래스를 작성합니다.
- 모든 Page 클래스는 공통 기능을 제공하는 `BasePage`를 상속합니다.
- Page 객체는 WebDriver 인스턴스 1개만 보유하며, 그 외 상태 변수를 최소화합니다.
- Page Layer와 Test Layer의 책임은 4절 기준을 따릅니다.

---

## 3. Project Structure (예정)

**아래 구조는 아직 생성되지 않은 예정 구조입니다.** 실제 구현을 시작하는 시점에 이 구조에 맞춰
생성합니다.

```
qa-process/
├── automation/
│   ├── pages/               # Page Object 클래스
│   │   ├── base_page.py
│   │   └── ...
│   ├── tests/                # 테스트 코드 (pytest)
│   │   ├── test_login.py
│   │   └── ...
│   ├── utils/                 # 화면과 무관한 공통 로직
│   ├── config/                 # 환경 설정(URL, 타임아웃 등)
│   ├── test_data/               # 정적 테스트 데이터(계정 이메일 등, 비밀번호 제외)
│   ├── screenshots/               # 실패 시 스크린샷(git 미추적)
│   ├── reports/                     # pytest-html/JUnit XML 리포트(git 미추적)
│   ├── conftest.py                   # pytest fixture
│   ├── pytest.ini                     # pytest 설정
│   └── requirements.txt                # Python 의존성
├── docs/                                # 기존 산출물(PRD/TC/Roadmap/Automation Guide)
├── scripts/sheets_sync/                  # 기존 Google Sheet 연동 스크립트(자동화 코드와 별개)
└── .github/workflows/                      # CI 워크플로우(미생성)
```

- `automation/` 하위 구조는 이 프로젝트의 자동화 코드 전용이며, 기존 `scripts/sheets_sync`
  (QA 프로세스 도구 스크립트)와는 목적이 다르므로 혼용하지 않습니다.
- 실제 디렉터리를 만들 때 위 구조와 다르게 조정해야 할 이유가 생기면, 이 문서를 먼저 갱신하고
  사용자 확인을 받은 뒤 반영합니다(CLAUDE.md 7절).

### 3.1 Import 경로 규칙

`automation/pytest.ini`가 저장소 루트가 아닌 `automation/` 디렉터리 안에 위치하고
`automation/` 자체에는 `__init__.py`가 없으므로, `automation/tests/`를 pytest로 실행하면
`automation/`이 사실상의 루트 패키지 경로가 된다(`automation`을 top-level 패키지로 인식하지
않음, 실측 확인됨 — 2026-08-27 Phase 0 Task 4).

- 모든 `automation/` 하위 코드(Page Object, 테스트, utils, config, test_data 등)는
  **`automation.` prefix 없이** `automation/` 자체를 루트로 삼아 import한다.
  - 올바른 예: `from pages.base_page import BasePage`, `from config.settings import BASE_URL`
  - 잘못된 예(실행 시 `ModuleNotFoundError` 발생): `from automation.pages.base_page import BasePage`
- 이 규칙은 `automation/` 하위 코드 사이의 상호 import에만 적용된다. `automation/` 바깥
  코드(`scripts/sheets_sync` 등)에서 `automation/` 코드를 import하는 시나리오는 현재
  범위에 없다.

---

## 4. Page Object / Layer 책임

### 4.1 Page Layer 책임

- 대상 화면의 모든 Locator를 클래스 상단에 상수로 정의합니다.
- 클릭/입력/스크롤 등 화면 조작 메서드를 제공합니다.
- 조회 메서드는 값을 **반환만** 합니다.
- **Assertion을 절대 수행하지 않습니다.**

### 4.2 Test Layer 책임

- Page 객체의 메서드를 호출해 시나리오를 구성합니다.
- 테스트에 필요한 데이터를 준비/정리합니다(11절 참고).
- Page에서 반환받은 값과 기대값을 비교해 **Assertion을 수행**합니다.
- 원칙: Page는 "어떻게 하는가", Test는 "무엇을 검증하는가"만 담당합니다.

```python
# pages/login_page.py
class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login-button")

    def login(self, email: str, password: str) -> None:
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)


# tests/test_login.py
def test_login_with_invalid_password(driver, login_page):
    login_page.login("actest1@test.com", "wrong-password")
    assert login_page.get_error_message() == "Your email or password is incorrect!"
```

---

## 5. 실제 페이지 탐색 규칙 (Playwright MCP 기반)

Selenium 코드를 작성하기 전 실제 페이지 구조와 Locator 후보를 조사·검증하는 개발 보조
도구로 **Playwright MCP**를 사용합니다(사용자 확정, 2026-08-27).

### 5.0 사전 준비 상태 (확인 완료)

**2026-08-27 기준으로 이 저장소/세션에 Playwright MCP 서버가 연결되어 있음을
확인했습니다**(`mcp__playwright__browser_snapshot`, `browser_evaluate`,
`browser_navigate` 등 도구 목록에서 확인됨). 이에 따라 아래 5.1~5.4 규칙을 실제
자동화 코드 작성 전 탐색 절차로 바로 적용할 수 있습니다. 서버 설정(설치/등록) 자체는
이 문서의 범위가 아닙니다.

### 5.1 사용 목적

- Playwright MCP는 Selenium 테스트 코드에 사용할 실제 페이지 구조와 Locator 후보를
  조사하고 검증하기 위한 **개발 보조 도구**로 사용합니다.
- 프로덕션 테스트 실행 도구는 **Selenium WebDriver**이며, Playwright MCP를 Selenium
  코드 실행 대신 사용하지 않습니다.

### 5.2 기본 탐색 순서

Selenium 코드를 작성하기 전에 다음 순서로 실제 페이지를 확인합니다.

1. 대상 기능의 Feature PRD(`docs/prd/feature/{slug}.md`)와 TC(`docs/tc/{slug}.md`)
   시나리오를 먼저 확인합니다.
2. Playwright MCP로 대상 페이지(`https://automationexercise.com/`)에 접근합니다.
3. `browser_snapshot`으로 페이지 구조와 대상 요소를 먼저 확인합니다.
4. snapshot만으로 정보가 부족하면 `browser_evaluate`로 DOM 속성을 확인합니다.
5. 확인한 정보를 기반으로 6절 우선순위에 따라 Selenium Locator를 작성합니다.
6. 작성한 Locator가 실제 대상 요소를 고유하게 식별하는지(동일 조건에 일치하는 요소가
   1개뿐인지) 검증합니다.

### 5.3 browser_evaluate 사용 기준

`browser_evaluate`는 다음 정보가 snapshot에서 충분히 확인되지 않을 때만 사용합니다.

- id, name, role, aria-label, placeholder
- data-testid 등 data-* 속성(실제 존재가 확인되는 경우에 한함)
- 대상 요소의 텍스트
- 상위·하위 DOM 관계
- 동일 조건에 일치하는 요소 개수

**금지**: 페이지 상태를 변경하거나 서비스 데이터를 조작하기 위한 JavaScript 실행(실제 계정
생성/삭제, 주문 시도 등)에는 사용하지 않습니다. Playwright MCP는 오직 **조회·탐색** 목적에만
한정하며, 승인되지 않은 Production 데이터 변경은 CLAUDE.md 11절 원칙을 그대로 따릅니다.

### 5.4 사용자 확인 요청 기준

다음 사유로 Playwright MCP를 이용한 직접 확인이 불가능한 경우에만 사용자에게 스크린샷이나
추가 정보를 요청합니다.

- 로그인 계정이나 권한이 없음
- OTP, 2FA 또는 CAPTCHA가 필요함
- 사내망이나 특정 네트워크 환경이 필요함
- 사용자별 데이터가 있어야 재현 가능함
- MCP 브라우저와 실제 테스트(Selenium) 환경이 다르게 동작함
- 대상 요소나 요구사항이 여러 의미로 해석될 수 있음

단순히 Locator가 제공되지 않았다는 이유만으로 작업을 중단하지 않습니다.

---

## 6. Locator 작성 원칙

### 6.1 우선순위

1. `id` 속성
2. `data-qa` 속성(테스트 전용 속성, 존재가 확인된 화면에 한함 — 아래 실측 근거 참고)
3. `name` 속성
4. 안정적인 CSS Selector(구조 변경에 덜 민감한 속성 기반)
5. 상대 XPath (텍스트/속성 결합 등 다른 방법으로 고유 식별이 어려울 때만, 최후 수단)

**Full XPath(`/html/body/div[1]/...`)는 절대 금지**합니다 — DOM 구조 변경에 매우 취약해
유지보수가 불가능합니다.

> 최초 작성 시점(2026-08-27)에는 `automationexercise.com`이 `data-testid` 같은 테스트
> 전용 속성을 제공하지 않는다고 보아 참고 프로젝트(`refer_CLAUDE.md`)의 "data-* 속성"
> 우선순위 단계를 제외했었습니다. 이후 Phase 1 Task 2(LoginPage 구현, 2026-08-29)에서
> automation-developer-agent가 Playwright MCP로 `/login` 페이지(로그인 폼 + 회원가입 폼)를
> 실측한 결과 `data-qa` 속성(예: `data-qa="login-email"`, `data-qa="login-password"`,
> `data-qa="login-button"`, `data-qa="signup-name"`, `data-qa="signup-email"`,
> `data-qa="signup-button"`)이 실제로 존재하며, 특히 `name="email"`이 같은 페이지 내
> 로그인/회원가입 두 폼에 중복 존재해 `name` 단독으로는 고유 식별이 불가능한 반면
> `data-qa`는 두 폼 사이에서 겹치지 않는 고유값임을 확인했습니다. 이에 따라 위 5절 원칙대로
> 우선순위를 갱신했습니다(사용자 승인, 2026-08-29). `data-qa`가 확인되지 않은 화면 요소는
> 이 우선순위를 적용할 수 없으므로 그대로 3순위(`name`)부터 적용합니다.

### 6.2 정의 위치

모든 Locator는 Page 클래스 상단에 `UPPER_SNAKE_CASE` 상수로 정의합니다. 메서드 내부에
Locator를 하드코딩하지 않습니다.

---

## 7. Wait 처리 원칙

- **`time.sleep()` 사용을 금지**합니다. 고정 시간 대기는 테스트를 느리고 불안정하게 만듭니다.
- Selenium의 `WebDriverWait` + `expected_conditions`로 **Explicit Wait**를 기본으로
  사용합니다.
- 반복되는 Wait 로직은 `BasePage`의 공통 메서드로 래핑합니다(예: `wait_and_click`,
  `wait_and_get_text` 등 — 실제 메서드명은 구현 시 확정).

---

## 8. Assertion 원칙

- Assertion은 **Test Layer에서만** 수행합니다(4.1절과 연결).
- pytest의 `assert`를 사용하며, 실패 메시지에 **기대값과 실제값을 모두 포함**합니다.

```python
assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"
```

---

## 9. Fixture 원칙

- WebDriver 생성/종료는 `conftest.py`의 fixture로 관리하며, `yield` 패턴으로 테스트 종료 후
  리소스 정리(`driver.quit()`)를 보장합니다.
- 기본 `scope`는 **`function`**으로 설정해 테스트마다 새 WebDriver를 생성합니다(10절 테스트
  독립성과 직결).
- 자주 쓰이는 Page 객체도 fixture로 제공해 테스트 코드의 반복을 줄입니다.

```python
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)
```

---

## 10. 테스트 독립성

- 각 테스트는 **단독 실행 가능**해야 하며, 다른 테스트의 실행 순서에 의존하지 않습니다.
- 각 테스트는 스스로 필요한 상태(로그인 등)를 셋업합니다.
- 테스트가 생성한 데이터(회원가입으로 만든 계정 등)는 가능한 범위에서 해당 테스트 내에서
  정리합니다(11절 데이터 관리 원칙과 연결).
- 이 원칙은 CLAUDE.md 10절 "Isolated/Reproducible/Idempotent" 원칙을 자동화 코드 수준에서
  구체화한 것입니다.

---

## 11. 테스트 데이터 관리

이 프로젝트는 dev/staging 없이 **Production 단일 환경**이고, 로그인에 재사용할 고정 계정
3개(`actest1~3@test.com`)와, 회원가입/계정삭제처럼 계정 자체를 생성·삭제하는 시나리오가
공존합니다. 이 특성을 반영해 **하이브리드 방식**을 채택합니다(사용자 승인 완료).

### 11.1 고정 계정 재사용 (로그인 상태가 필요한 시나리오)

- 로그인/로그아웃, 장바구니, 상품 상세 등 "이미 존재하는 계정으로 로그인"이 필요한 TC는
  사전 준비된 계정 3개를 재사용합니다.
- 계정 **이메일**은 `test_data/accounts.json` 등 설정 파일로 관리합니다.
- 계정 **비밀번호**는 어떤 파일에도 하드코딩하지 않고 `.env`(환경변수)로만 관리합니다
  (12절 참고).

### 11.2 동적 생성 (계정을 생성/삭제하는 시나리오)

- 회원가입, 계정삭제 TC처럼 매 실행마다 신규 계정이 필요한 경우, `utils`의 Factory 함수로
  임의 이메일을 동적 생성합니다(예: `f"test_{uuid.uuid4().hex[:8]}@example.com"`).
- 이렇게 하면 고정 계정이 삭제 테스트로 소모되는 사고를 방지하고, Production 데이터 오염을
  최소화할 수 있습니다(CLAUDE.md 11절 "테스트 간 데이터 오염과 의존성 최소화").
- 생성한 계정을 테스트 내에서 정리(삭제)할 수 있는 경우, 가능한 범위에서 정리합니다.

### 11.3 공통 원칙

- 테스트 데이터를 코드에 직접 하드코딩하지 않습니다.
- Production 데이터(실제 사용자 데이터 등)를 생성/수정/삭제하는 작업은 CLAUDE.md 11절에
  따라 사용자의 명시적 승인 없이 수행하지 않습니다. 여기서 다루는 "계정 생성/삭제"는 TC에서
  이미 승인된 테스트 목적의 계정에 한정합니다.

---

## 12. 환경변수 및 민감정보 관리

- 비밀번호 등 민감정보는 코드에 절대 작성하지 않고 환경변수로 관리합니다
  (`python-dotenv` + `.env`).
- `.env`는 `.gitignore`에 포함해 git에 커밋되지 않도록 합니다(이미 프로젝트
  `.gitignore`에 `.env` 규칙이 존재하며, 자동화 코드용 변수도 동일한 방식을 따릅니다).
- CI(GitHub Actions) 환경에서는 GitHub Secrets로 관리합니다(CLAUDE.md 17절과 동일).
- 로그, 리포트(HTML/JUnit XML), 실패 스크린샷 어디에도 비밀번호 등 민감정보가 노출되지
  않도록 합니다.

---

## 13. Logging

- `print()` 대신 Python 표준 `logging` 모듈을 사용합니다.
- 로그 레벨 기준:
  - `DEBUG`: Locator 탐색, 요소 상태 등 상세 진단 정보
  - `INFO`: 로그인, 페이지 이동, 클릭 등 주요 액션
  - `WARNING`: 재시도, 느린 응답 등
  - `ERROR`: 예외 발생, 요소를 찾지 못함 등
  - `CRITICAL`: 드라이버 크래시 등 심각한 오류
- 비밀번호 등 민감정보는 로그에 마스킹 처리합니다.
- 로그 저장 경로/포맷/로테이션 방식은 실제 구현 시 확정합니다(현재 미정).

---

## 14. 실패 시 Screenshot / Artifact

- pytest hook(`pytest_runtest_makereport`)을 이용해 테스트 **실패 시에만** 자동으로
  스크린샷을 캡처합니다.
- 파일명 규칙: `{테스트_함수명}_{상태}_{YYYY-MM-DD_HH-MM-SS}.png`
- 저장 위치: `automation/screenshots/`(git 미추적)
- 스크린샷에 민감정보(비밀번호 입력값 등)가 노출되지 않도록 주의합니다.
- CI 실행 시 실패 스크린샷과 리포트(pytest-html, JUnit XML)는 GitHub Actions Artifact로
  업로드해 사후 확인이 가능하도록 합니다(16절 CI/CD와 연결, 실제 워크플로우 파일은 별도
  단계에서 작성 — CLAUDE.md 15절).

---

## 15. Exception Handling

- 프로젝트 전역 CLAUDE.md "에러 핸들링 필수" 원칙을 자동화 코드에서는 다음과 같이
  구체화합니다.
- 불필요하게 광범위한 `except Exception:` 처리를 지양하고, Selenium이 실제로 발생시키는
  구체적 예외(`TimeoutException`, `NoSuchElementException` 등)를 명시적으로 처리합니다.
- 예외 발생 시 반드시 로그를 남겨(`logger.error(...)`) 이후 디버깅이 가능하게 합니다.
- 예외를 조용히 삼키지 않습니다(로깅 없이 `pass` 처리 금지).

---

## 16. CI/CD

- GitHub Actions를 사용하며, **GitHub Push 시 자동으로 자동화 테스트가 실행**됩니다.
- 실행 흐름(CLAUDE.md 15절과 동일): `Git Push → GitHub Actions → 자동화 테스트 실행 →
  Test Report 생성 → 결과 판정 → Slack Notification`
- **실패 시 Slack 알림에는 어떤 부분(테스트/Feature)에서 실패했는지 알 수 있는 정보를
  포함**합니다. JUnit XML 결과를 파싱해 실패한 테스트 이름과 사유 요약을 메시지에 포함하는
  방식을 사용합니다(1절 리포팅 결정과 연결).
- 이 문서는 CI **운영 원칙**만 정의하며, 실제 GitHub Actions Workflow(YAML) 파일과 Slack
  연동 스크립트는 별도 구현 단계에서 작성합니다(CLAUDE.md 15절과 동일한 범위 제한).
- Slack은 결과 알림 전용이며 Commit/Push 승인 용도로 사용하지 않습니다(CLAUDE.md 16절).

---

## 17. Coding Convention

- 1.1절의 "코딩 스타일 예외"에 따라 **PEP8**을 기준으로 합니다.
  - 들여쓰기: 4칸
  - 한 줄 최대 길이: 100자 권장
  - 타입힌트를 함수 파라미터/반환값에 권장(가독성 확보)
- 주석은 프로젝트 전역 CLAUDE.md에 따라 **한국어**로 작성합니다.
- 변수명/함수명은 영어를 사용합니다(전역 CLAUDE.md "변수명/함수명: 영어" 원칙 유지, 표기법만
  1.1절 예외에 따라 snake_case).

---

## 18. Naming Convention

| 대상 | 규칙 | 예시 |
|---|---|---|
| 파일명 | snake_case | `login_page.py`, `test_login.py` |
| 클래스명 | PascalCase | `LoginPage`, `BasePage` |
| Page 객체 클래스 | `Page` 접미사 필수 | `LoginPage` (O), `Login` (X) |
| 메서드명 | snake_case, 동사로 시작 | `click_login_button`, `get_error_message` |
| 테스트 함수명 | `test_` 접두사 | `test_login_with_valid_credentials` |
| 변수명 | snake_case | `search_keyword`, `product_count` |
| 상수(Locator 등) | UPPER_SNAKE_CASE | `LOGIN_BUTTON`, `EMAIL_INPUT` |

---

## 19. 공통 코드 분리 기준

- **2회 이상 반복**되는 코드는 공통 메서드/함수로 분리합니다(CLAUDE.md 12절 "불필요한 중복
  구현 금지"와 연결).
- **BasePage**: 모든 Page에서 필요한 공통 화면 조작(요소 찾기, 클릭, Wait 래핑 등).
- **utils**: 화면과 무관한 순수 로직(랜덤 데이터 생성, 문자열/날짜 처리 등).
- 특정 Feature 하나에서만 쓰이는 로직을 섣불리 공통화하지 않습니다(과도한 추상화 지양).

---

## 20. 테스트 실행 및 검증

- 코드 작성 후에는 **반드시 관련 테스트를 실행**해 동작을 검증합니다. 실행 없이 "완료"로
  간주하지 않습니다(CLAUDE.md 13절과 동일).
- 실행 예시:
  ```bash
  # 특정 파일 실행
  pytest automation/tests/test_login.py

  # 전체 실행 + HTML/JUnit 리포트 생성
  pytest automation/tests/ --html=automation/reports/report.html --junitxml=automation/reports/results.xml
  ```
- 테스트 실패 시 원인을 CLAUDE.md 13절의 4가지 범주(Automation Code / Test Data / Test
  Environment / 실제 Product 문제) 중 하나로 구분하려고 시도하며, 원인이 불명확하면 추측으로
  결론 내리지 않고 사용자에게 보고합니다.
- 실패를 회피하기 위해 무한/반복적으로 재시도하지 않습니다.

---

## 21. 코드 작성 후 Self Review 체크리스트

코드 작성을 완료로 보고하기 전에 다음을 자체 점검합니다.

- [ ] `time.sleep()`을 사용하지 않았는가? (Explicit Wait 사용)
- [ ] Full XPath를 사용하지 않았는가?
- [ ] 모든 Locator가 Page 클래스 상단에 상수로 정의되어 있는가?
- [ ] Page Layer에 Assertion이 없는가?
- [ ] 모든 Page 클래스가 `BasePage`를 상속하는가?
- [ ] 각 테스트가 다른 테스트 실행 순서에 의존하지 않는가?
- [ ] 계정 정보/비밀번호가 코드에 하드코딩되지 않았는가?
- [ ] `print()` 대신 `logging`을 사용했는가?
- [ ] 예외를 광범위하게 처리하지 않고 구체적으로 처리·로깅했는가?
- [ ] 파일명(snake_case)/클래스명(PascalCase, `~Page` 접미사)/함수명(snake_case,
      동사 시작)/테스트 함수명(`test_` 접두사) 규칙을 지켰는가?
- [ ] 4칸 들여쓰기를 사용했는가?
- [ ] 코드 작성 후 실제로 pytest를 실행해 결과(PASSED/FAILED/ERROR)를 확인했는가?
- [ ] 실패 시 스크린샷이 저장되었는가?
- [ ] (Locator를 새로 작성한 경우) 5절 절차에 따라 Playwright MCP로 실제 페이지 구조를
      확인하고 Locator의 고유성을 검증했는가?

---

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-27 | 최초 작성. `refer_CLAUDE.md` 분석 및 사용자 확인(자동화 대상 범위, 언어/프레임워크,\
 데이터 관리, 리포팅, CI/CD 등)을 거쳐 초안 작성 및 즉시 사용자 승인. | 승인완료 |
| 2026-08-27 | 자동화 코드 작성 전 실제 페이지 구조를 확인할 개발 보조 도구가 필요해 "5. 실제\
 페이지 탐색 규칙" 절 신규 추가(사용자 요청). 이에 따라 5절 이후 절 번호를 전체 재정렬하고,\
 기존 절 번호 참조 오류 2건(2절의 "5절"→"4절", Fixture 절의 "9절"→"10절", Screenshot 절의\
 "15절"→"16절", Tech Stack 표의 "9절"→"16절")을 함께 수정. | 승인완료 |
| 2026-08-27 | 5절의 도구를 claude-in-chrome Skill에서 **Playwright MCP**로 변경(사용자\
 확정 — 이 프로젝트에서 Playwright MCP를 사용하기로 결정). 단, 2026-08-27 기준 이 세션에\
 Playwright MCP 서버가 아직 연결되어 있지 않음을 5.0절에 명시(실제 사용 전 서버 연결 확인\
 필요). | 승인완료 |
| 2026-08-27 | 5.0절 갱신: 이 세션 도구 목록에서 Playwright MCP 서버(`mcp__playwright__*`)\
 연결이 확인되어, "미연결" 상태를 "연결 확인 완료"로 수정(사용자 확인). | 승인완료 |
| 2026-08-27 | Phase 0 Task 4(conftest.py/config 작성) 구현 중 automation-developer-agent가\
 실제 pytest 실행으로 재현·확인한 사실을 반영해 "3.1 Import 경로 규칙" 절 신규 추가\
 (automation/pytest.ini 위치상 automation. prefix import가 실제로는 동작하지 않고\
 automation/을 루트로 삼는 import만 동작함, 사용자 승인 완료). | 승인완료 |
| 2026-08-29 | Phase 1 Task 2(LoginPage 구현) 중 automation-developer-agent가 Playwright MCP로\
 `/login` 페이지를 실측해 `data-qa` 속성이 실제로 존재함을 확인(로그인/회원가입 두 폼에서\
 `name="email"`이 중복되어 `name` 단독으로는 고유 식별 불가함도 함께 확인)한 사실을 반영해\
 6.1절 Locator 우선순위에 `data-qa`(2순위, id 다음 name 이전)를 추가(사용자 승인 완료). | 승인완료 |
