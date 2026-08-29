"""로그인 페이지(/login)를 다루는 Page Object.

Source of Truth:
- docs/tc/login-logout.md (TC-LOGIN-LOGOUT-001~006, 010, 013)
- docs/prd/feature/login-logout.md 3절 로그인 시나리오
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-29, https://automationexercise.com/login):
- Email/Password 입력란은 로그인 폼과 회원가입 폼 모두에서 name 속성이 "email"로 중복되어
  (실측: input[name="email"]이 페이지 내 2개) name 단독으로는 고유하지 않음을 확인했다.
  대신 실제 페이지에 data-qa 속성(예: data-qa="login-email", data-qa="login-password",
  data-qa="login-button")이 존재하며 두 폼 사이에서 서로 겹치지 않는 고유값임을 확인해,
  AUTOMATION_GUIDE 6.1절 3순위("안정적인 CSS Selector") 범주 내에서 data-qa 기반 CSS
  속성 선택자를 사용한다.
- "Login to your account"/"New User Signup!" 제목(h2) 영역은 id/name/data-qa가 없어
  각각의 상위 컨테이너 클래스(.login-form, .signup-form)로 범위를 좁힌 CSS Selector를
  사용했다(각 컨테이너 내 h2가 1개뿐임을 실측으로 확인).
- 에러 메시지(ERROR_MESSAGE) Locator는 최초 작성 시점(2026-08-29 Task 2)에는 로그아웃
  상태의 정상 진입 화면에서 DOM에 렌더링되지 않아 직접 확인이 불가능해 확신도 낮음으로
  잠정 작성했었다. **2026-08-29 Task 5(automation-developer-agent, TC-LOGIN-LOGOUT-005/006/013
  실제 pytest 실행)에서 존재하지 않는 이메일/잘못된 비밀번호/긴 특수문자 입력 3가지 실패
  케이스 모두 `.login-form p` Locator가 "Your email or password is incorrect!" 텍스트를
  정확히 반환함을 실행 로그(PASSED)로 확인했다.** 수정 없이 그대로 유효함이 실측으로
  확정되었다.
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    """로그인 페이지(/login)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/type_text/get_text/is_element_visible)만 사용해 요소를 조작·조회한다.
    """

    # "Login to your account" 영역
    LOGIN_FORM_HEADING = (By.CSS_SELECTOR, ".login-form h2")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")

    # 로그인 실패 시 폼 하단에 노출되는 에러 메시지(REQ-LOGIN-LOGOUT-005)
    # 실측 완료(2026-08-29 Task 5) - TC-005/006/013 pytest 실행으로 정상 동작 확인(위 docstring 참고)
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".login-form p")

    # "New User Signup!" 영역
    NEW_USER_SIGNUP_HEADING = (By.CSS_SELECTOR, ".signup-form h2")

    def navigate(self) -> None:
        """로그인 페이지(/login)로 이동한다."""
        url = f"{BASE_URL}login"
        self.driver.get(url)
        self.logger.info("로그인 페이지로 이동: %s", url)

    def login(self, email: str, password: str) -> None:
        """Email Address/Password를 입력하고 Login 버튼을 클릭한다.

        비밀번호 등 민감정보는 BasePage.type_text가 입력값을 로깅하지 않으므로(로케이터만
        로깅) 이 메서드 호출로 인해 비밀번호가 로그에 노출되지 않는다.
        """
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """로그인 실패 시 노출되는 에러 메시지 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.ERROR_MESSAGE)

    def click_new_user_signup(self) -> None:
        """"New User Signup!" 영역을 클릭한다."""
        self.click(self.NEW_USER_SIGNUP_HEADING)

    def is_login_form_visible(self) -> bool:
        """"Login to your account" 로그인 폼 제목 영역의 노출 여부를 반환한다."""
        return self.is_element_visible(self.LOGIN_FORM_HEADING)

    def is_new_user_signup_visible(self) -> bool:
        """"New User Signup!" 영역(회원가입 진입 영역)의 노출 여부를 반환한다."""
        return self.is_element_visible(self.NEW_USER_SIGNUP_HEADING)
