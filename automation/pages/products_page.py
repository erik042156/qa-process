"""Products 페이지(/products)를 다루는 Page Object.

Source of Truth:
- docs/tc/top-navigation.md (TC-TOP-NAVIGATION-001, 002, 004, 005)
- docs/prd/feature/top-navigation.md 상단 네비게이션 시나리오
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-30, https://automationexercise.com/products,
로그아웃 상태):
- 상단 네비게이션(`ul.navbar-nav`, 실제 class 속성값 "nav navbar-nav") 하위 8개 `<li><a>`
  (Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video Tutorials/Contact us)가
  `home_page.py`가 실측한 Home 페이지(`/`)와 완전히 동일한 마크업 구조임을
  browser_evaluate로 재확인했다(class/개수/id·data-qa·name 부재 여부 모두 동일). 이에
  따라 HomePage와 동일하게 4순위(안정적인 CSS Selector, href 기반)를 사용한다.
- **HomePage와의 차이점(중요)**: Products 페이지에서는 `a[href='/']`,
  `a[href='/view_cart']`가 페이지 전체 기준으로 **고유하지 않음**을
  `document.querySelectorAll(...)`.length로 실측 확인했다.
  - `a[href='/']`은 2개 존재 — 상단 네비게이션의 "Home" 메뉴(`<a href="/"><i
    class="fa fa-home"></i> Home</a>`) 외에, 헤더 로고 이미지 링크(`<a href="/"><img
    src="/static/images/home/logo.png" ...></a>`)가 동일 href를 가진다.
  - `a[href='/view_cart']`도 2개 존재 — 상단 네비게이션의 "Cart" 메뉴 외에, "Add to
    cart" 확인 모달 내부의 "View Cart" 링크(`<a href="/view_cart"><u>View
    Cart</u></a>`)가 동일 href를 가진다(Products 목록 페이지는 상품 카드마다 "Add to
    cart" 모달을 갖고 있어 이 중복 요소가 DOM에 존재한다).
  - 따라서 `HOME_LINK`는 `ul.navbar-nav` 컨테이너로 범위를 좁힌 CSS Selector
    (`ul.navbar-nav a[href='/']`)를 사용해 고유성을 확보했다
    (`document.querySelectorAll("ul.navbar-nav a[href='/']").length === 1`로 검증
    완료). `a[href='/view_cart']`도 동일하게 2개 존재함을 확인했으나, Approved TC
    (TC-TOP-NAVIGATION-001~006) 중 Products 페이지에서 "Cart" 메뉴를 클릭해야 하는
    TC가 없어(TC-004/005는 `navigate()`로 페이지를 직접 이동) 2026-08-31 코드 리뷰에서
    미사용(dead code)으로 지적되어 `CART_LINK`/`click_cart()`를 제거했다(CLAUDE.md
    12절 "불필요한 코드 생성 금지"). 이후 Phase에서 실제로 필요해지면 이 실측 근거를
    참고해 다시 추가하면 된다.
  - 반면 `SIGNUP_LOGIN_LINK`(`a[href='/login']`)는 Products 페이지에서도 페이지 전체
    기준 1개뿐임을 재확인해(HomePage와 동일), 범위를 좁히지 않고 그대로 재사용한다.

로그인 상태 전용 Locator(LOGOUT_LINK, DELETE_ACCOUNT_LINK, LOGGED_IN_AS_TEXT) 처리 근거:
- Playwright MCP는 조회·탐색 전용 도구로 실제 로그인 상태를 만들 수 없어(AUTOMATION_GUIDE
  5.3절), 이 Task에서는 Products 페이지에서 직접 실측하지 못했다. 다만 `home_page.py`가
  2026-08-29 Task 5(실제 pytest 실행, 고정 계정 actest1로 실제 로그인)에서 이미 실측
  확정한 `a[href='/logout']`, `a[href='/delete_account']`,
  `//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]` 3개
  Locator와 위에서 재확인한 대로 Products 페이지의 `ul.navbar-nav` 컨테이너가 Home
  페이지와 완전히 동일한 구조라는 근거로 동일 값을 그대로 사용한다. **로그인 상태에서의
  최종 검증은 이 Task의 범위가 아니며, 후속 테스트 Task(pytest 실행)에서 실제 로그인 후
  확인된다.**
- 로그아웃 상태 DOM에는 `/logout`, `/delete_account` 링크가 존재하지 않음(각 0개)을
  Products 페이지에서도 재확인했다(HomePage와 동일한 서버 조건부 렌더링 방식).
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """Products 페이지(/products)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text/is_element_visible/find_element)만 사용해 요소를 조작·조회한다.
    화면 단위 1 Page 클래스 원칙에 따라 HomePage와 마크업 패턴은 유사하지만 별도 클래스로
    구현한다(Phase 2의 AccountCreatedPage/AccountDeletedPage와 동일한 설계 결정).
    """

    # 상단 네비게이션 - Playwright MCP 실측 확인 완료(위 docstring 참고)
    # HOME_LINK는 페이지 내 중복 href(로고)와 구분하기 위해 ul.navbar-nav 컨테이너로
    # 범위를 좁혔다(HomePage와의 차이점, 위 docstring 참고).
    HOME_LINK = (By.CSS_SELECTOR, "ul.navbar-nav a[href='/']")

    # 상단 네비게이션(로그아웃 상태) - Playwright MCP 실측 확인 완료(HomePage와 동일값)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    # 상단 네비게이션(로그인 상태) - HomePage 실측 결과를 근거로 동일 값 사용(위 docstring
    # 참고, 최종 검증은 후속 테스트 Task에서 수행)
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGGED_IN_AS_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]",
    )

    # 상단 네비게이션 메뉴 구성 전체 조회용(ul.navbar-nav 하위 모든 li>a, 8개 실측 확인)
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "ul.navbar-nav li > a")

    def navigate(self) -> None:
        """Products 페이지(/products)로 이동한다."""
        url = f"{BASE_URL.rstrip('/')}/products"
        self.driver.get(url)
        self.logger.info("Products 페이지로 이동: %s", url)

    def click_home(self) -> None:
        """"Home" 메뉴를 클릭한다.

        [Phase 3 Task, 2026-08-30 실측] TC-TOP-NAVIGATION-001 pytest 실행 중 재현·확인한
        결함: 이 메뉴 클릭이 실제 페이지 전체 이동(`<a href="/">`)을 트리거하는데, 클릭 직후
        Google Vignette 전면 광고(뷰포트 전체를 덮는 iframe)가 개입해 URL이
        `.../products#google_vignette`에 머물고 실제 Home으로 이동하지 못하는 현상을
        독립 재현 스크립트로 확인했다(BasePage.click_and_retry_if_vignette() docstring에
        이미 기술된 것과 동일한 결함 패턴). `click()` 대신 이미 검증된
        `click_and_retry_if_vignette()`를 사용해 1회 재클릭으로 우회한다.
        """
        self.click_and_retry_if_vignette(self.HOME_LINK)

    def is_logged_out_menu_visible(self) -> bool:
        """로그아웃 상태 메뉴("Signup / Login")의 노출 여부를 반환한다."""
        return self.is_element_visible(self.SIGNUP_LOGIN_LINK)

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

    def get_nav_menu_item_texts(self) -> list[str]:
        """상단 네비게이션 메뉴 전체 항목의 텍스트를 순서대로 조회해 반환한다(Assertion 없음).

        `BasePage`에는 다건 조회 메서드가 없으므로, 먼저 `find_element()`로 첫 메뉴 항목이
        DOM에 로드될 때까지 명시적으로 대기한 뒤 `driver.find_elements()`(복수형)로 전체
        메뉴 항목을 한 번에 조회한다.
        """
        self.find_element(self.NAV_MENU_ITEMS)
        elements = self.driver.find_elements(*self.NAV_MENU_ITEMS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("상단 네비게이션 메뉴 텍스트 조회 완료: %s", texts)
        return texts
