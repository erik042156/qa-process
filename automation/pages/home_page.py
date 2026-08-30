"""Home 페이지(/)를 다루는 Page Object.

Source of Truth:
- docs/tc/login-logout.md (TC-LOGIN-LOGOUT-004, 014, 015)
- docs/prd/feature/login-logout.md 3절 로그인/로그아웃 시나리오, REQ-LOGIN-LOGOUT-003/004/014
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-29, https://automationexercise.com/, 로그아웃 상태):
- 상단 네비게이션(`ul.navbar-nav`, 실제 class 속성값 "nav navbar-nav") 하위 8개 `<li><a>`
  (Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video Tutorials/Contact us)를
  browser_evaluate로 전수 조회한 결과, 8개 항목 모두 id/data-qa/name 속성이 존재하지 않음을
  확인했다(AUTOMATION_GUIDE 6.1절 1~3순위 적용 불가). 이에 따라 4순위(안정적인 CSS Selector)로
  각 링크의 href 속성을 사용했다.
- "Signup / Login" 메뉴는 `a[href='/login']`이 페이지 전체에서 1개뿐임을
  `document.querySelectorAll('a[href="/login"]').length === 1`로 실측 확인해 고유성을
  검증했다.
- 로그아웃 상태 DOM에는 `/logout`, `/delete_account` 링크가 아예 존재하지 않는다(숨김 처리가
  아니라 서버가 로그인 상태에 따라 다른 HTML을 렌더링하는 방식으로 판단됨 — LoginPage의
  ERROR_MESSAGE 사례와 동일하게 서버 렌더링 조건부 마크업).

로그인 상태 전용 Locator(LOGOUT_LINK, DELETE_ACCOUNT_LINK, LOGGED_IN_AS_TEXT) 실측 확인 결과:
- 최초 작성 시점(2026-08-29 Task 2)에는 Playwright MCP로 실제 로그인(폼 제출/상태 변경)을
  수행할 수 없어(AUTOMATION_GUIDE 5.3절, 조회·탐색 전용 원칙) 확신도 낮음으로 잠정
  작성했었다. **2026-08-29 Task 5(automation-developer-agent, TC-LOGIN-LOGOUT-004 실제
  pytest 실행, 고정 계정 actest1로 실제 로그인)에서 `a[href='/logout']`,
  `a[href='/delete_account']`, `//ul[contains(@class, 'navbar-nav')]//a[contains(text(),
  'Logged in as')]` 3개 Locator 모두 로그인 성공 직후 Home 페이지에서 정상적으로 요소를
  찾고 텍스트를 반환함을 실행 로그(PASSED)로 확인했다.** 로그아웃 상태와 동일한
  `ul.navbar-nav` 컨테이너 구조를 로그인 상태에서도 재사용한다는 기존 추정이 실측으로
  확정되었으며, 수정 없이 그대로 유효하다.

Phase 3 확장(PRODUCTS_LINK/CART_LINK/NAV_MENU_ITEMS 추가, Playwright MCP 실측,
2026-08-30, https://automationexercise.com/, 로그아웃 상태):
- TC-TOP-NAVIGATION-002(Products 클릭)/003(Cart 클릭)/004·005(메뉴 구성 조회)를
  Home 페이지에서도 자동화하기 위해 products_page.py/cart_page.py와 동일한 패턴으로
  PRODUCTS_LINK, CART_LINK, NAV_MENU_ITEMS를 추가했다. ProductsPage/CartPage 구현
  시 발견된 "동일 href를 가진 요소가 페이지 전체에 중복 존재" 패턴이 Home 페이지에도
  있는지 추측하지 않고 document.querySelectorAll(...).length로 직접 실측했다.
- a[href='/products']: 페이지 전체 기준 1개(고유함). ProductsPage/CartPage와 달리
  Home 페이지의 Featured Items/Recommended Items 캐러셀 상품 카드는
  /product_details/{id}로 링크하며 /products로 링크하는 요소가 없어 중복이 발생하지
  않는다. 이에 따라 기존 SIGNUP_LOGIN_LINK와 동일하게 ul.navbar-nav로 범위를 좁히지
  않고 a[href='/products']를 그대로 사용한다.
- a[href='/view_cart']: 페이지 전체 기준 2개 존재(고유하지 않음) - 상단 네비게이션의
  "Cart" 메뉴(<a href="/view_cart"><i class="fa fa-shopping-cart"></i> Cart</a>,
  ul.navbar-nav 하위) 외에, Home 페이지의 상품 카드에서 "Add to cart" 클릭 시 뜨는
  확인 모달 내부의 "View Cart" 링크(<a href="/view_cart"><u>View Cart</u></a>,
  modal-body 하위, DOM에 항상 존재하며 모달 노출 여부와 무관하게 querySelectorAll에
  포함됨)가 동일 href를 가진다(ProductsPage와 동일한 원인 패턴). 이에 따라
  ProductsPage/CartPage와 동일하게 ul.navbar-nav 컨테이너로 범위를 좁힌 CSS
  Selector(ul.navbar-nav a[href='/view_cart'])를 사용해 고유성을 확보했다
  (document.querySelectorAll("ul.navbar-nav a[href='/view_cart']").length === 1로
  검증 완료).
- ul.navbar-nav 하위 8개 li>a 구조(href/텍스트)를 재확인한 결과, 기존 docstring에
  기록된 구조(Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video
  Tutorials/Contact us)와 완전히 동일함을 확인했다.
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home 페이지(/)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text/is_element_visible)만 사용해 요소를 조작·조회한다.
    """

    # 상단 네비게이션(로그아웃 상태) - Playwright MCP 실측 확인 완료(위 docstring 참고)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    # 상단 네비게이션(로그인 상태) - 실측 완료(2026-08-29 Task 5, 위 docstring 참고)
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGGED_IN_AS_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]",
    )

    # 상단 네비게이션(Phase 3 확장) - Playwright MCP 실측 확인 완료(위 docstring 참고)
    # 실측 시점(2026-08-30)에는 PRODUCTS_LINK가 페이지 전체 기준으로도 고유했으나,
    # 2026-08-31 코드 리뷰에서 "다른 모든 동종 Locator(CART_LINK 포함, ProductsPage/
    # CartPage의 대응 Locator 전부)는 ul.navbar-nav로 범위를 좁혔는데 이것만 예외라
    # 향후 페이지에 /products로 연결되는 배너/캐러셀이 추가되면 조용히 엉뚱한 요소를
    # 클릭할 수 있다"는 지적을 받아, 일관성과 견고성을 위해 동일하게 스코핑했다
    # (재실측 없이도 ul.navbar-nav a[href='/products']는 기존에 고유했던
    # a[href='/products']의 부분집합이므로 여전히 유효).
    PRODUCTS_LINK = (By.CSS_SELECTOR, "ul.navbar-nav a[href='/products']")
    CART_LINK = (By.CSS_SELECTOR, "ul.navbar-nav a[href='/view_cart']")

    # 상단 네비게이션 메뉴 구성 전체 조회용(ul.navbar-nav 하위 모든 li>a, 8개 실측 확인)
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "ul.navbar-nav li > a")

    def navigate(self) -> None:
        """Home 페이지(루트 URL)로 이동한다."""
        self.driver.get(BASE_URL)
        self.logger.info("Home 페이지로 이동: %s", BASE_URL)

    def is_logged_out_menu_visible(self) -> bool:
        """로그아웃 상태 메뉴("Signup / Login")의 노출 여부를 반환한다."""
        return self.is_element_visible(self.SIGNUP_LOGIN_LINK)

    def click_signup_login(self) -> None:
        """"Signup / Login" 메뉴를 클릭한다.

        [2026-08-31 코드 리뷰 반영] click_logout()/click_delete_account()/
        click_products()/click_cart()와 동일하게 실제 페이지 전체 이동
        (`<a href="/login">`)을 트리거하므로 Google Vignette 전면 광고 개입 위험이
        동일하게 있어, `click()` 대신 `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.SIGNUP_LOGIN_LINK)

    def is_logged_in_menu_visible(self) -> bool:
        """로그인 상태 메뉴(Logout, Delete Account)의 노출 여부를 반환한다.

        두 메뉴가 모두 노출되는 경우에만 True를 반환한다.
        """
        return self.is_element_visible(self.LOGOUT_LINK) and self.is_element_visible(
            self.DELETE_ACCOUNT_LINK
        )

    def get_logged_in_user_text(self) -> str:
        """"Logged in as {유저명}" 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.LOGGED_IN_AS_TEXT)

    def click_logout(self) -> None:
        """"Logout" 메뉴를 클릭한다.

        [2026-08-31 Phase 3 Task 7 회귀 실행 중 발견] 이 메뉴도 click_products()/
        click_cart()와 동일하게 실제 페이지 전체 이동(`<a href="/logout">`)을
        트리거하므로 Google Vignette 전면 광고가 개입할 수 있는 동일한 위험이
        있다(당시에는 click_delete_account()에서만 실제로 재현되어 발견되었으나,
        같은 클릭 방식을 쓰는 이 메서드에도 선제적으로 동일 방어를 적용한다).
        `click()` 대신 이미 검증된 `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.LOGOUT_LINK)

    def click_delete_account(self) -> None:
        """"Delete Account" 메뉴를 클릭한다.

        [2026-08-31 Phase 3 Task 7 회귀 실행 중 발견] Phase 1+2+3 통합 회귀
        실행(28건) 중 `test_continue_from_account_deleted_lands_on_home`가 2회
        연속 동일하게 실패했다. 실패 스크린샷을 확인한 결과 이 메뉴 클릭 직후
        Google Vignette 전면 광고 오버레이가 화면을 덮은 채 URL이 `/delete_account`
        로 전환되지 않았다(`click_products()`/`click_cart()`/`click_home()`이 이미
        겪었던 것과 동일한 결함 패턴, AUTOMATION_GUIDE 7.1절 참고). 이 메서드만
        일반 `click()`을 쓰고 있어 방어가 없었던 것이 원인으로 확인되어, `click()`
        대신 이미 검증된 `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.DELETE_ACCOUNT_LINK)

    def click_products(self) -> None:
        """"Products" 메뉴를 클릭한다.

        [Phase 3 Task, 2026-08-30 실측] TC-TOP-NAVIGATION-002 pytest 실행 중 재현·확인한
        결함: 이 메뉴 클릭이 실제 페이지 전체 이동(`<a href="/products">`)을 트리거하는데,
        클릭 직후 Google Vignette 전면 광고(뷰포트 전체를 덮는 iframe)가 개입해 URL이
        `...#google_vignette`에 머물고 실제 Products로 이동하지 못하는 현상을 독립
        재현 스크립트로 확인했다(BasePage.click_and_retry_if_vignette() docstring에 이미
        기술된 것과 동일한 결함 패턴). `click()` 대신 이미 검증된
        `click_and_retry_if_vignette()`를 사용해 1회 재클릭으로 우회한다.
        """
        self.click_and_retry_if_vignette(self.PRODUCTS_LINK)

    def click_cart(self) -> None:
        """"Cart" 메뉴를 클릭한다.

        [Phase 3 Task, 2026-08-30] click_products()와 동일한 이유(Google Vignette 전면
        광고가 페이지 전체 이동 클릭 직후 개입할 수 있음)로 `click()` 대신
        `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.CART_LINK)

    def get_nav_menu_item_texts(self) -> list[str]:
        """상단 네비게이션 메뉴 전체 항목의 텍스트를 순서대로 조회해 반환한다(Assertion 없음).

        `BasePage`에는 다건 조회 메서드가 없으므로, 먼저 `find_element()`로 첫 메뉴 항목이
        DOM에 로드될 때까지 명시적으로 대기한 뒤 `driver.find_elements()`(복수형)로 전체
        메뉴 항목을 한 번에 조회한다(ProductsPage/CartPage와 동일한 구현 패턴).
        """
        self.find_element(self.NAV_MENU_ITEMS)
        elements = self.driver.find_elements(*self.NAV_MENU_ITEMS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("상단 네비게이션 메뉴 텍스트 조회 완료: %s", texts)
        return texts
