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

    def navigate(self) -> None:
        """Home 페이지(루트 URL)로 이동한다."""
        self.driver.get(BASE_URL)
        self.logger.info("Home 페이지로 이동: %s", BASE_URL)

    def is_logged_out_menu_visible(self) -> bool:
        """로그아웃 상태 메뉴("Signup / Login")의 노출 여부를 반환한다."""
        return self.is_element_visible(self.SIGNUP_LOGIN_LINK)

    def click_signup_login(self) -> None:
        """"Signup / Login" 메뉴를 클릭한다."""
        self.click(self.SIGNUP_LOGIN_LINK)

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
        """"Logout" 메뉴를 클릭한다."""
        self.click(self.LOGOUT_LINK)
