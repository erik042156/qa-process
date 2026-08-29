---
문서유형: Automation Development Roadmap
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
관련 Feature PRD: [feature/login-logout.md, feature/signup-delete-account.md, feature/top-navigation.md, feature/product-search.md, feature/cart.md, feature/product-detail.md, feature/page-ui.md]
관련 Automation Candidate 문서: [tc/automation-candidates/login-logout.md, tc/automation-candidates/signup-delete-account.md, tc/automation-candidates/top-navigation.md, tc/automation-candidates/product-search.md, tc/automation-candidates/cart.md, tc/automation-candidates/product-detail.md, tc/automation-candidates/page-ui.md]
관련 Automation Guide: docs/automation/AUTOMATION_GUIDE.md
최초 작성일: 2026-08-27
최근 변경일: 2026-08-29
승인일: 2026-08-27
---

# ROADMAP - Automation Exercise QA 자동화 개발 Roadmap

## 1. 개요 및 범위

이 문서는 `qa-process` 프로젝트에서 자동화 대상으로 확정된 Test Case를 기반으로,
개발팀이 순서대로 실행할 수 있는 자동화 코드 개발 실행 계획을 정의한다.

**대상 정의**: 아래 조건을 모두 만족하는 TC만 이 Roadmap의 구현 대상 범위로 삼는다.

```
Candidate 문서(docs/tc/automation-candidates/{slug}.md) 상태 = 자동화대상확정
AND
QA Decision = Approved
```

**대상 Feature 및 확정 TC 수 총계**: `docs/tc/automation-candidates/` 하위 7개 문서
전체(login-logout, cart, page-ui, product-detail, product-search,
signup-delete-account, top-navigation)를 재조회한 결과, 7개 Feature 모두
`상태: 자동화대상확정`이며 아래와 같이 총 **75건**의 TC가 최종 자동화 대상으로 확정되어
있다.

| Feature | 확정(Approved) TC 수 |
|---|---|
| login-logout | 11 |
| signup-delete-account | 11 |
| top-navigation | 6 |
| product-search | 7 |
| cart | 13 |
| product-detail | 6 |
| page-ui | 21 |
| **합계** | **75** |

이 수치는 `AUTOMATION_GUIDE.md` 0.1절의 2026-08-27 스냅샷(13/11/21/6/7/11/6)과 항목별로
정확히 일치한다. 다만 이 Roadmap의 대상 확정 근거는 스냅샷 재사용이 아니라, 아래 "2. 입력
문서 스냅샷"과 "8. 리스크 및 확인 필요 사항"에 기록한 대로 각 Candidate 문서와 원본 TC
문서를 직접 재조회하여 별도로 검증한 결과다.

**Out of Scope(이 Roadmap이 다루지 않는 범위)**:
- Shrimp Task 생성 및 세부 작업 분해 (별도 단계, 이 Roadmap 승인 이후 진행)
- 실제 자동화 코드 구현 (별도 단계)
- 자동화 코드의 언어/프레임워크/네이밍 등 구체적 작성 방식 — Source of Truth는
  `docs/automation/AUTOMATION_GUIDE.md`이며 이 문서는 "무엇을 어떤 순서로 만들 것인가"만
  다룬다.

## 2. 입력 문서 스냅샷

| 문서 | 상태 | 최근 변경일 |
|---|---|---|
| prd/project-prd.md | 승인완료 | 2026-08-22 |
| prd/feature/login-logout.md | 승인완료 | 2026-08-20 |
| prd/feature/signup-delete-account.md | 승인완료 | 2026-08-20 |
| prd/feature/top-navigation.md | 승인완료 | 2026-08-21 |
| prd/feature/product-search.md | 승인완료 | 2026-08-21 |
| prd/feature/cart.md | 승인완료 | 2026-08-21 |
| prd/feature/product-detail.md | 승인완료 | 2026-08-21 |
| prd/feature/page-ui.md | 승인완료 | 2026-08-22 |
| tc/login-logout.md | 승인완료 | 2026-08-22 |
| tc/signup-delete-account.md | 승인완료 | 2026-08-22 |
| tc/top-navigation.md | 승인완료 | 2026-08-22 |
| tc/product-search.md | 승인완료 | 2026-08-22 |
| tc/cart.md | 승인완료 | 2026-08-22 |
| tc/product-detail.md | 승인완료 | 2026-08-22 |
| tc/page-ui.md | 승인완료 | 2026-08-22 |
| tc/automation-candidates/login-logout.md | 자동화대상확정 | 확정일 2026-08-24 |
| tc/automation-candidates/signup-delete-account.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/top-navigation.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/product-search.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/cart.md | 자동화대상확정 | 확정일 2026-08-24 |
| tc/automation-candidates/product-detail.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/page-ui.md | 자동화대상확정 | 확정일 2026-08-24 |
| automation/AUTOMATION_GUIDE.md | 승인완료 | 2026-08-27 |

**재확인 결과(Workflow 2단계)**: 7개 Candidate 문서의 "Approved TC 목록(자동화 대상 확정)"에
기재된 TC ID 전건(75건)이 각 원본 TC 문서(`docs/tc/{slug}.md`)에 실제로 존재함을
grep으로 재확인했고, 7개 원본 TC 문서 모두 여전히 `상태: 승인완료`이며, 각 Candidate
문서의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(전 Feature 공통 2026-08-22)이 현재
원본 TC 문서의 "최근 변경일"과 정확히 일치해 평가 이후 원본 TC가 변경된 사실이 없음을
확인했다. 불일치는 발견되지 않았다(상세는 8절 참조).

## 3. 기술 스택 및 아키텍처 (Reference)

`AUTOMATION_GUIDE.md` 1~4절 요약이며, 상세 규칙은 원본 문서를 기준으로 한다.

- 언어/도구: Python + Selenium WebDriver + pytest, 리포팅은 pytest-html(HTML) +
  JUnit XML(`--junitxml`) 병행. 브라우저는 Chrome(ChromeDriver). 대상 환경은 Production
  단일 환경(`https://automationexercise.com/`).
- 코딩 스타일: PEP8 예외 적용(4칸 들여쓰기, snake_case) — 전역 CLAUDE.md의 2칸/camelCase
  규칙에 대한 Python 자동화 코드 한정 예외(사용자 승인 완료).
- 아키텍처: Page Object Model(POM). 화면 단위 1 Page 클래스, 모든 Page는 `BasePage` 상속.
  Page Layer는 조작/조회만 담당(Assertion 없음), Test Layer가 Assertion을 전담.
- 디렉터리 구조(예정): `automation/pages`, `automation/tests`, `automation/utils`,
  `automation/config`, `automation/test_data`, `automation/screenshots`(git 미추적),
  `automation/reports`(git 미추적), `automation/conftest.py`, `automation/pytest.ini`,
  `automation/requirements.txt`.
- 테스트 데이터: 로그인 상태가 필요한 시나리오는 고정 계정 3개(`actest1~3@test.com`,
  이메일은 `test_data/accounts.json`, 비밀번호는 `.env`) 재사용. 회원가입/계정삭제처럼
  계정 자체를 생성·삭제하는 시나리오는 `utils`의 Factory 함수로 임의 이메일 동적 생성.

## 4. 구현 순서 결정 기준

**1순위: 기능적 의존성**
- 로그인 상태가 필요한 시나리오(장바구니 체크아웃 진입, 상단 네비게이션 로그인 상태
  메뉴, Checkout 페이지 UI 등)가 다수 존재하므로, 로그인/로그아웃(LoginPage 및 인증
  상태 확보)이 다른 모든 Feature의 전제 조건이 된다.
- 장바구니에 상품이 담긴 상태가 필요한 시나리오(Checkout 진입, page-ui의 Checkout/Cart
  비어있지 않은 상태 UI)가 있으므로, Cart의 핵심 담기/조회 메커니즘이 page-ui의 일부
  TC보다 먼저 준비되어야 한다.
- "Add to Cart" 확인 모달은 `cart.md`(REQ-CART-001)가 원 정의이며 `product-detail.md`가
  이를 참조·재사용한다고 PRD/Candidate 문서에 명시되어 있으므로, 공유 컴포넌트의 중복
  정의를 피하기 위해 cart를 product-detail보다 먼저 구현한다.
- 회원가입/계정삭제는 로그인 페이지(`/login`)의 "New User Signup!" 영역에서 시작되므로
  로그인/로그아웃과 동일한 화면(LoginPage)을 공유한다. 다른 Feature를 기능적으로 막지는
  않지만, Page Object 재사용 효율을 위해 로그인/로그아웃 바로 다음에 배치한다.

**2순위: Priority / Business Criticality / Automation Score**
- 기능적 의존관계가 동등한 Feature 사이에서는 Candidate 문서의 Business Criticality/
  Automation Score, 그리고 원본 TC의 Priority(P0 비중)를 참고해 순서를 정한다. 다만
  점수만으로 기계적으로 정하지 않고, Feature 간 결합도(공용 Page Object 재사용 가능성)를
  함께 고려한다.
- 상품 검색(product-search)은 로그인/장바구니 상태와 무관하게 독립적으로 수행 가능한
  Feature이며, Products 페이지 검색 결과 카드가 page-ui의 ALL PRODUCTS 그리드 카드 구조를
  참조하지만 이는 완전한 선행 조건은 아니므로(별도 Risk Coverage), 로그인 이후 이른
  시점에 독립적으로 배치한다.
- 각 페이지별 UI(page-ui)는 21건으로 대상 TC 수가 가장 많고 Home/Products/Cart/
  Signup-Login/Checkout 5개 화면을 모두 다루지만, 그중 다수(Checkout 관련 TC-025~039 등)가
  "로그인 + 장바구니에 상품이 담긴 상태"라는 다른 Feature의 산출물을 전제로 하므로 순서상
  가장 나중에 배치한다. 이렇게 하면 이전 Phase에서 이미 만들어진 HomePage/ProductsPage/
  CartPage/LoginPage/CheckoutPage Page Object를 그대로 확장해 재사용할 수 있다.

## 5. Phase별 Roadmap

### Phase 0: 공통 기반 구축 (Foundation)

- 산출물: `automation/` 디렉터리 구조 생성(pages/tests/utils/config/test_data/
  screenshots/reports), `BasePage`(공통 요소 탐색·클릭·입력·Wait 래핑 메서드),
  `conftest.py`(WebDriver fixture, function scope), `config/`(Base URL, 타임아웃 등),
  `test_data/accounts.json` 템플릿, `.env` 템플릿(비밀번호 등 민감정보 자리, 실제 값은
  커밋하지 않음), `requirements.txt`, `pytest.ini`.
- 근거: AUTOMATION_GUIDE 2, 3, 9, 11, 12절.
- 이 Phase가 끝나야 이후 모든 Feature Phase가 시작 가능하다(모든 Page 클래스가
  `BasePage`를 상속하고, 모든 테스트가 `driver` fixture를 사용).

### Phase 1: 로그인 / 로그아웃 (login-logout) 자동화 구현

- 대상 TC: 11건 (TC-LOGIN-LOGOUT-001, 002, 003, 004, 005, 006, 010, 011, 013, 014, 015)
- 필요 Page Object: `LoginPage`(로그인 폼 조작/에러 메시지 조회, "New User Signup!" 영역
  진입점 포함), `HomePage`(로그인 성공 후 랜딩 확인용 최소 골격)
- 선행 조건(의존 Feature): 없음 (Phase 0 완료 후 최우선 착수)
- 우선순위 근거: 장바구니 체크아웃 진입, 상단 네비게이션 로그인 상태 메뉴, page-ui의
  Checkout 화면 등 다른 다수 Feature의 TC가 "로그인 상태"를 전제 조건으로 요구하므로
  기능적 의존성상 최우선. Business Criticality도 최상위(다수 TC가 Score 25~26, P0 다수
  포함 — 로그인 Happy Path, 로그아웃 핵심 동작 등).

### Phase 2: 회원가입 / 계정삭제 (signup-delete-account) 자동화 구현

- 대상 TC: 11건 (TC-SIGNUP-DELETE-ACCOUNT-001, 002, 004, 005, 006, 007, 010, 011, 012,
  013, 014)
- 필요 Page Object: `SignupPage`(상세 정보 입력 페이지 `/signup`), `AccountCreatedPage`
  (`/account_created` 완료 화면), `AccountDeletedPage`(`/delete_account` 완료 화면),
  `LoginPage` 확장(Phase 1에서 만든 클래스의 "New User Signup!" 섹션 메서드 재사용/보강)
- 선행 조건(의존 Feature): login-logout — 같은 `/login` 화면(LoginPage)에서 회원가입
  플로우가 시작되고, 삭제된 계정 재로그인 검증(TC-SIGNUP-DELETE-ACCOUNT-013)이 Phase 1의
  로그인 에러 메시지 검증 로직을 재사용한다.
- 우선순위 근거: LoginPage를 공유하는 화면이라 Page Object 재사용 효율이 높고, 회원가입/
  계정삭제 Happy Path가 다수 P0(Score 25~26)로 Business Criticality가 매우 높다. 이후
  Phase에서 필요한 "동적 계정 생성" Factory 유틸리티(11.2절)도 이 Phase에서 함께 마련된다.
- **[Phase 1 인수 사항]** Phase 1에서 구현된 `LoginPage.click_new_user_signup()`(automation/pages/login_page.py)은
  "New User Signup!" 제목(h2) 영역을 클릭하는 구조로 구현되어 있으나, 실측 결과 해당 h2에는
  클릭 핸들러가 없어 클릭 자체가 실질적 효과가 없다(automation-developer-agent 2026-08-29
  보고, Playwright MCP 실측 기반). Phase 1의 Approved TC는 이 메서드를 요구하지 않아 Phase 1
  범위에서는 문제가 없었지만, 이 Phase(회원가입)는 실제로 Name/Email 입력 후 Signup 버튼을
  클릭해 `/signup`으로 진입해야 하므로, 이 메서드를 그대로 재사용하지 말고 signup-form의
  Name/Email 입력 필드와 Signup 버튼(Task 2 구현 시 확인된 data-qa 속성 후보: signup-name,
  signup-email, signup-button)을 사용하는 방식으로 재작업이 필요하다. 실제 재작업 여부와
  구체적 구현은 Phase 2 착수 시점에 automation-developer-agent가 재확인 후 진행한다.

### Phase 3: 상단 네비게이션 (top-navigation) 자동화 구현

- 대상 TC: 6건 (TC-TOP-NAVIGATION-001~006)
- 필요 Page Object: `HomePage`/`ProductsPage`/`CartPage`의 네비게이션 관련 메서드
  확장(메뉴 클릭, 이동 URL 확인, "Logged in as {유저명}" 조회, 활성 표시 조회)
- 선행 조건(의존 Feature): login-logout — 로그인 상태/로그아웃 상태 각각에서 메뉴 구성
  일관성(REQ-TOP-NAVIGATION-005)과 "Logged in as {유저명}" 표시(REQ-TOP-NAVIGATION-006)를
  검증하려면 Phase 1에서 확보한 로그인/로그아웃 상태 전환 메커니즘이 선행되어야 한다.
- 우선순위 근거: 기능적 의존성(로그인 상태 필요) 외에, 이 Phase에서 확장하는 HomePage/
  ProductsPage/CartPage의 기본 네비게이션 메서드는 이후 product-search/cart/product-detail/
  page-ui Phase에서 공통으로 재사용되므로 이른 시점에 배치해 결합도 높은 공용 Page Object를
  먼저 안정화한다.

### Phase 4: 상품 검색 (product-search) 자동화 구현

- 대상 TC: 7건 (TC-PRODUCT-SEARCH-001, 002, 003, 004, 005, 006, 008)
- 필요 Page Object: `ProductsPage` 확장(검색창 입력, 검색 실행, 검색 결과 카드/제목/URL
  조회)
- 선행 조건(의존 Feature): 없음 (로그인/로그아웃 상태와 무관하게 수행 가능한 독립
  Feature). 다만 Phase 3에서 이미 만들어진 `ProductsPage` 기본 골격을 확장하는 형태로
  구현한다.
- 우선순위 근거: 기능적으로 다른 Feature를 막지 않는 독립 Feature이므로, 로그인 관련
  기반(Phase 1~3)이 갖춰진 직후 낮은 결합도의 Feature부터 처리한다. 검색 실행/URL 변경/
  매칭 로직 등 다수 TC가 결정적 판정이 가능하고 Score 20~23 수준으로 중요도가 있다.

### Phase 5: 장바구니 (cart, 상품 담기 포함) 자동화 구현

- 대상 TC: 13건 (TC-CART-001, 002, 003, 004, 005, 006, 008, 009, 010, 011, 014, 015, 016)
- 필요 Page Object: `CartPage`(장바구니 목록/삭제/빈 카트 상태), `AddToCartModal`
  (Home/Products 리스트 페이지 공용 담기 확인 모달 — 이후 product-detail Phase가 재사용할
  공유 컴포넌트로 이 Phase에서 최초 정의), `CheckoutPage`(로그인 요구 모달 및 `/checkout`
  기본 골격), `HomePage`/`ProductsPage`의 "Add to cart" 메서드 확장
- 선행 조건(의존 Feature): login-logout — "Proceed To Checkout" 클릭 시 로그인 상태별
  분기(REQ-CART-008/009), 로그인/로그아웃 상태에 따른 장바구니 병합·복원 동작
  (TC-CART-014~016) 검증에 Phase 1의 로그인/로그아웃 메커니즘이 필요하다.
- 우선순위 근거: Business Criticality가 매우 높은 TC(수량/합계 계산, 체크아웃 진입,
  로그인 상태별 데이터 정합성 등 다수 Score 24~26)가 다수 포함되어 있고, "Add to Cart"
  확인 모달의 원 정의를 담당하는 Feature이므로 이를 재사용하는 product-detail보다
  먼저 구현한다.

### Phase 6: 상품 상세 (product-detail) 자동화 구현

- 대상 TC: 6건 (TC-PRODUCT-DETAIL-001, 002, 008, 015, 016, 021)
- 필요 Page Object: `ProductDetailPage`(신규) — Quantity 입력/스피너, Add to cart 버튼,
  가격/카테고리 등 조회 메서드. "Add to cart" 확인 모달은 Phase 5에서 정의한
  `AddToCartModal`을 재사용(신규 정의하지 않음).
- 선행 조건(의존 Feature): cart — REQ-PRODUCT-DETAIL-016이 참조하는 담기 확인 모달은
  cart Feature(REQ-CART-001)가 원 정의이므로, Page Object 중복 정의를 피하려면 cart
  Phase 이후에 진행한다. login-logout에는 기능적으로 의존하지 않는다(비로그인 상태에서도
  상세 페이지 접근/담기 가능).
- 우선순위 근거: URL 패턴(진입점, Score 23), 정상 진입 스모크 테스트(Score 25), Add to
  cart 모달 재검증(Score 23) 등 중요도가 있으나, cart의 모달 정의에 의존하는 결합 관계상
  cart 다음으로 배치한다.

### Phase 7: 각 페이지별 UI (page-ui) 자동화 구현

- 대상 TC: 21건 (TC-PAGE-UI-006, 009, 015, 019, 020, 021, 023, 024, 025, 026, 028, 029,
  030, 031, 032, 033, 034, 035, 036, 037, 039)
- 필요 Page Object: `HomePage`/`ProductsPage`(배너·캐러셀, CATEGORY/BRANDS 아코디언,
  FEATURES ITEMS/ALL PRODUCTS 그리드, RECOMMENDED ITEMS 캐러셀 조회 메서드 확장),
  `CartPage`(빈 카트 안내, Proceed To Checkout 버튼, 상품 목록 표 컬럼 조회 확장),
  `CheckoutPage`(Address Details, Review Your Order, Total Amount, Place Order 버튼 조회
  확장 — Phase 5에서 만든 골격을 확장), `CategoryProductsPage`/`BrandProductsPage`(신규,
  카테고리/브랜드 필터링 결과 페이지)
- 선행 조건(의존 Feature): login-logout, cart — Checkout 관련 다수 TC(034~037, 039 등)는
  "로그인 상태 + 장바구니에 상품이 담긴 상태"에서 `/checkout` 페이지에 진입해야 확인
  가능하므로, 두 Feature의 Page Object/메커니즘이 이미 준비되어 있어야 효율적으로
  구현·재사용할 수 있다.
- 우선순위 근거: 대상 TC 수가 21건으로 가장 많지만, Home/Products/Cart/Signup-Login/
  Checkout 5개 화면을 모두 다루는 넓은 범위이며 다수 TC가 이미 다른 Phase에서 구축된
  Page Object의 확장으로 구현 가능하다. 따라서 공용 Page Object 재사용을 극대화하기 위해
  가장 마지막 Feature Phase로 배치한다.

### Phase Final: CI/CD 및 Slack 알림 연동

- 산출물: `.github/workflows/` 워크플로우(Push 시 자동화 테스트 실행 → 리포트 생성 →
  결과 판정), Slack 실패 알림 스크립트(JUnit XML 파싱, 실패 테스트명/사유 요약 포함)
- 근거: AUTOMATION_GUIDE 16절, CLAUDE.md 15/16절.
- 이 Phase는 Phase 1~7에서 생성된 자동화 테스트 스위트가 최소 1회 이상 로컬에서
  PASSED/FAILED로 실행 검증된 이후 착수한다.

## 6. Feature별 상세 매핑표

| Feature | 확정 TC 수 | 대상 TC ID | 필요 Page Object | 의존 Feature | Phase |
|---|---|---|---|---|---|
| login-logout | 11 | TC-LOGIN-LOGOUT-001, 002, 003, 004, 005, 006, 010, 011, 013, 014, 015 | LoginPage, HomePage(골격) | 없음 | Phase 1 |
| signup-delete-account | 11 | TC-SIGNUP-DELETE-ACCOUNT-001, 002, 004, 005, 006, 007, 010, 011, 012, 013, 014 | SignupPage, AccountCreatedPage, AccountDeletedPage, LoginPage(확장) | login-logout | Phase 2 |
| top-navigation | 6 | TC-TOP-NAVIGATION-001~006 | HomePage/ProductsPage/CartPage(네비게이션 확장) | login-logout | Phase 3 |
| product-search | 7 | TC-PRODUCT-SEARCH-001, 002, 003, 004, 005, 006, 008 | ProductsPage(검색 확장) | 없음 | Phase 4 |
| cart | 13 | TC-CART-001, 002, 003, 004, 005, 006, 008, 009, 010, 011, 014, 015, 016 | CartPage, AddToCartModal, CheckoutPage(골격), HomePage/ProductsPage(Add to cart 확장) | login-logout | Phase 5 |
| product-detail | 6 | TC-PRODUCT-DETAIL-001, 002, 008, 015, 016, 021 | ProductDetailPage(신규), AddToCartModal(재사용) | cart | Phase 6 |
| page-ui | 21 | TC-PAGE-UI-006, 009, 015, 019, 020, 021, 023, 024, 025, 026, 028, 029, 030, 031, 032, 033, 034, 035, 036, 037, 039 | HomePage/ProductsPage/CartPage/CheckoutPage(확장), CategoryProductsPage, BrandProductsPage(신규) | login-logout, cart | Phase 7 |

## 7. Definition of Done

각 Feature Phase는 다음을 모두 충족해야 완료로 간주한다.

- AUTOMATION_GUIDE 20절 기준으로 해당 Phase의 pytest를 실제로 실행해 PASSED/FAILED/
  ERROR 결과를 확인했는가 (실행 없이 "완료"로 간주하지 않음).
- AUTOMATION_GUIDE 21절 Self Review 체크리스트(Explicit Wait 사용, Full XPath 미사용,
  Locator 상수화, Page Layer에 Assertion 없음, `BasePage` 상속, 테스트 독립성, 민감정보
  미하드코딩, `logging` 사용, 구체적 예외 처리, Naming Convention, 4칸 들여쓰기, 실패 시
  스크린샷 저장, 신규 Locator의 Playwright MCP 검증)를 모두 충족했는가.
- 코드 리뷰가 완료되었는가(CLAUDE.md 3절 워크플로우 7단계, Roadmap Agent의 책임 범위
  밖이며 후속 리뷰 단계에서 수행).
- 테스트 실패가 발생한 경우 원인을 Automation Code / Test Data / Test Environment / 실제
  Product 문제 중 하나로 구분하려 시도했으며, 불명확한 경우 추측으로 결론짓지 않고
  사용자에게 보고했는가.

## 8. 리스크 및 확인 필요 사항

**검증 결과 요약**: 7개 Candidate 문서와 7개 원본 TC 문서를 전수 재조회한 결과, 아래와
같이 **불일치나 결함은 발견되지 않았다.**

- TC ID 유효성: 75건의 Approved TC ID 전건이 각 원본 TC 문서에 실제로 존재함을 grep으로
  재확인했다.
- 원본 TC 문서 상태: 7개 문서 모두 여전히 `상태: 승인완료`이다.
- 원본 TC 변경 여부: 7개 Candidate 문서의 "대상 TC 문서 최근 변경일(평가 시점 기준)"이
  모두 2026-08-22이며, 현재 원본 TC 문서의 "최근 변경일"과 정확히 일치해 평가 이후 원본이
  변경된 사실이 없다.
- 관련 Feature PRD 7건 모두 `상태: 승인완료`이다.
- `AUTOMATION_GUIDE.md` 0.1절 스냅샷(13/11/21/6/7/11/6)과 이번 재조회 결과가 Feature별로
  정확히 일치해, 스냅샷 이후 자동화 대상 범위에 드리프트가 없음을 확인했다(단, 이 일치는
  스냅샷을 신뢰해 도출한 것이 아니라 별도 재조회로 검증한 결과다).

**사용자 확인이 필요한 판단 사항(이 Roadmap 초안에서 에이전트가 판단해 제안한 내용)**:

1. **Phase 순서 판단**: PRD/Candidate 문서에 "Feature 구현 순서" 자체가 명시적으로
   정의되어 있지 않으므로, 4절에 기술한 기능적 의존성(로그인 필요 여부, Add to Cart 모달
   공유 관계 등)과 Page Object 재사용 효율을 근거로 에이전트가 Phase 1~7 순서를
   판단했다. 특히 다음 두 가지는 PRD에 명시된 필수 순서가 아니라 에이전트의 구현 효율
   판단이므로 사용자 검토가 필요하다.
   - signup-delete-account를 top-navigation보다 먼저 배치(LoginPage 공유에 따른 재사용
     효율 근거, 기능적 강제 의존은 아님).
   - cart를 product-detail보다 먼저 배치(Add to Cart 모달의 원 정의 Feature를 먼저
     구현해 중복 정의를 피하려는 근거, 기능적 강제 의존은 아님 — product-detail 단독으로도
     구현 자체는 가능함).
2. **Cross-Feature 중복/참고 항목**: Candidate 문서 자체에 이미 기록되어 있던 사항이며
   이 Roadmap에서 새로 발견한 문제는 아니지만, 참고로 안내한다.
   - `page-ui.md` TC-PAGE-UI-040/041은 `cart.md` TC-CART-012/013과 검증 목적이 사실상
     동일해 두 문서 모두 QA Decision: Rejected로 일관되게 정리되어 있다(자동화 대상에서
     이미 제외됨, 조치 불필요).
   - `product-search.md` TC-PRODUCT-SEARCH-002(검색 결과 카드 구성)는 `page-ui.md`
     TC-PAGE-UI-015(ALL PRODUCTS 그리드 카드 구성)와 동일한 카드 컴포넌트를 검증하지만
     별도 Risk Coverage(검색 필터링 경로)로 판단되어 둘 다 Approved로 확정되어 있다.
     Page Object 관점에서는 두 TC가 동일한 상품 카드 Locator를 공유하게 되므로, 구현 단계
     (Shrimp Task 분해 이후)에서 중복 Locator 정의가 발생하지 않도록 유의가 필요하다는
     점만 참고로 남긴다(이 Roadmap 문서 자체의 범위 밖).
3. **[Phase 1 구현 중 발견, 2026-08-29 추가] LoginPage.click_new_user_signup() Phase 2 재작업
   필요 가능성**: Phase 1 Task 2(LoginPage 구현) 실측 결과 "New User Signup!" 클릭 메서드가
   실질적 효과가 없는 구조로 확인되었다. 5절 Phase 2 항목에 인수 사항으로 기록해두었으며,
   Phase 2 착수 시 실제 재작업 필요 여부를 다시 판단한다(현재는 사용자에게 미리 알리는
   목적의 예고 기록이며, 이 자체가 Roadmap의 Phase 순서나 범위를 변경하지는 않는다).

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-27 | 최초 작성. `docs/tc/automation-candidates/` 7개 문서 전체를 재조회하여 자동화대상확정 Feature 7개(login-logout, cart, page-ui, product-detail, product-search, signup-delete-account, top-navigation)를 확인하고, 원본 TC 문서와의 정합성(TC ID 존재, 승인완료 상태, 원본 변경 여부)을 재검증(불일치 없음). 관련 Feature PRD 7건 및 Project PRD를 확인해 기능적 의존성(로그인 필요 여부, Add to Cart 모달 공유 관계 등)을 근거로 Phase 1~7 순서를 판단해 초안 작성. 사용자 검토 대기 중. | 초안 |
| 2026-08-27 | 사용자가 8절에 기록된 판단 필요 사항 두 가지(1. signup-delete-account를 top-navigation보다 먼저 배치, 2. cart를 product-detail보다 먼저 배치)에 대해 "1,2번 승인"으로 동의. 이후 Roadmap 전체에 대한 최종 승인 여부를 별도로 재확인한 결과 사용자가 "네, 승인합니다"라고 명확한 최종 승인 의사를 밝힘. | 승인완료 |
| 2026-08-29 | 사용자 재승인에 따른 부분 갱신. Phase 1 Task 2(LoginPage 구현) 완료 후 automation-developer-agent가 보고한 리스크(`click_new_user_signup()`이 클릭 핸들러 없는 h2를 클릭하는 구조라 Phase 2에서 재작업이 필요할 수 있음)를 5절 Phase 2 항목과 8절 리스크 목록에 인수 사항으로 기록. Phase 순서/범위/Definition of Done 등 기존 내용은 변경하지 않음. | 승인완료 |
