"""Cart 페이지(/view_cart)를 다루는 Page Object.

Source of Truth:
- docs/tc/top-navigation.md (TC-TOP-NAVIGATION-003, 004, 005)
- docs/prd/feature/top-navigation.md 상단 네비게이션 시나리오
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-30, https://automationexercise.com/view_cart,
로그아웃 상태, 빈 장바구니 상태):
- 상단 네비게이션(`ul.navbar-nav`, 실제 class 속성값 "nav navbar-nav") 하위 8개 `<li><a>`
  (Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video Tutorials/Contact us)가
  `home_page.py`/`products_page.py`가 실측한 구조와 완전히 동일한 마크업임을
  browser_evaluate로 재확인했다(class/개수/href 값 모두 동일). 이에 따라 HomePage/
  ProductsPage와 동일하게 4순위(안정적인 CSS Selector, href 기반)를 사용한다.
- **HOME_LINK/PRODUCTS_LINK 고유성 실측 결과(중요)**: Cart 페이지에서도 ProductsPage와
  마찬가지로 `a[href='/']`, `a[href='/products']`가 페이지 전체 기준으로 **고유하지
  않음**을 `document.querySelectorAll(...).length`로 실측 확인했다.
  - `a[href='/']`은 페이지 전체 기준 **3개** 존재 — 상단 네비게이션의 "Home" 메뉴
    (`<a href="/"><i class="fa fa-home"></i> Home</a>`) 외에, 헤더 로고 이미지 링크
    (`<a href="/"><img src="/static/images/home/logo.png" ...></a>`), 그리고 Cart
    페이지 상단 브레드크럼의 "Home" 링크(`<a href="/">Home</a>`, 브레드크럼은
    ProductsPage/HomePage에는 없는 Cart 페이지 고유 요소)까지 총 3개가 동일 href를
    가진다(ProductsPage의 2개보다 1개 더 많음 — 브레드크럼 때문).
  - `a[href='/products']`도 페이지 전체 기준 **2개** 존재 — 상단 네비게이션의
    "Products" 메뉴 외에, 실측 시점에 장바구니가 비어 있어 노출된 "Cart is empty!
    Click here to buy products." 안내 메시지의 "here" 링크
    (`<a href="/products"><u>here</u></a>`)가 동일 href를 가진다.
  - `ul.navbar-nav` 컨테이너로 범위를 좁히면(`ul.navbar-nav a[href='/']`,
    `ul.navbar-nav a[href='/products']`) 각각 고유해짐을
    (`document.querySelectorAll(...).length === 1`로) 검증했으나, Approved TC
    (TC-TOP-NAVIGATION-001~006) 중 Cart 페이지에서 "Home"/"Products" 메뉴를 클릭해야
    하는 TC가 없어(TC-004/005는 `navigate()`로 페이지를 직접 이동) 2026-08-31 코드
    리뷰에서 미사용(dead code)으로 지적되어 `HOME_LINK`/`PRODUCTS_LINK`와
    `click_home()`/`click_products()`를 제거했다(CLAUDE.md 12절 "불필요한 코드 생성
    금지"). 이후 Phase에서 실제로 필요해지면 이 실측 근거를 참고해 다시 추가하면 된다.
  - 반면 `SIGNUP_LOGIN_LINK`(`a[href='/login']`)는 Cart 페이지에서도 페이지 전체
    기준 1개뿐임을 재확인해(HomePage/ProductsPage와 동일), 범위를 좁히지 않고 그대로
    재사용한다.

로그인 상태 전용 Locator(LOGOUT_LINK, DELETE_ACCOUNT_LINK, LOGGED_IN_AS_TEXT) 처리 근거:
- Playwright MCP는 조회·탐색 전용 도구로 실제 로그인 상태를 만들 수 없어(AUTOMATION_GUIDE
  5.3절), 이 Task에서는 Cart 페이지에서 직접 실측하지 못했다. 다만 `home_page.py`가
  2026-08-29 Task 5(실제 pytest 실행, 고정 계정 actest1로 실제 로그인)에서 이미 실측
  확정하고 `products_page.py`가 동일 `ul.navbar-nav` 구조 근거로 재사용한
  `a[href='/logout']`, `a[href='/delete_account']`,
  `//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]` 3개
  Locator를, 이 Task에서 재확인한 Cart 페이지의 `ul.navbar-nav` 컨테이너가 Home/Products
  페이지와 완전히 동일한 구조라는 근거로 동일하게 재사용한다. **로그인 상태에서의 최종
  검증은 이 Task의 범위가 아니며, 후속 테스트 Task(pytest 실행)에서 실제 로그인 후
  확인된다.**
- 로그아웃 상태 DOM에는 `/logout`, `/delete_account` 링크가 존재하지 않음(각 0개)을
  Cart 페이지에서도 재확인했다(HomePage/ProductsPage와 동일한 서버 조건부 렌더링 방식).
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class CartPage(BasePage):
    """Cart 페이지(/view_cart)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text/is_element_visible/find_element)만 사용해 요소를 조작·조회한다.
    화면 단위 1 Page 클래스 원칙에 따라 HomePage/ProductsPage와 마크업 패턴은 유사하지만
    별도 클래스로 구현한다(ProductsPage와 동일한 설계 결정).
    """

    # 상단 네비게이션(로그아웃 상태) - Playwright MCP 실측 확인 완료(HomePage/ProductsPage와 동일값)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    # 상단 네비게이션(로그인 상태) - HomePage/ProductsPage 실측 결과를 근거로 동일 값 사용
    # (위 docstring 참고, 최종 검증은 후속 테스트 Task에서 수행)
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGGED_IN_AS_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]",
    )

    # 상단 네비게이션 메뉴 구성 전체 조회용(ul.navbar-nav 하위 모든 li>a, 8개 실측 확인)
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "ul.navbar-nav li > a")

    def navigate(self) -> None:
        """Cart 페이지(/view_cart)로 이동한다."""
        url = f"{BASE_URL.rstrip('/')}/view_cart"
        self.driver.get(url)
        self.logger.info("Cart 페이지로 이동: %s", url)

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
        메뉴 항목을 한 번에 조회한다(ProductsPage와 동일한 구현 패턴).
        """
        self.find_element(self.NAV_MENU_ITEMS)
        elements = self.driver.find_elements(*self.NAV_MENU_ITEMS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("상단 네비게이션 메뉴 텍스트 조회 완료: %s", texts)
        return texts
