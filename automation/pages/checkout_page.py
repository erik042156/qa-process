"""로그인 요구 모달(id="checkoutModal") 및 `/checkout` 진입 골격을 다루는 Page Object.

Source of Truth:
- docs/tc/cart.md (TC-CART-010, 011)
- docs/prd/feature/cart.md REQ-CART-008/009
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

[Phase 5 범위 한정] ROADMAP.md Phase 5 항목에 따라 이 Page Object는 "로그인 요구 모달 +
`/checkout` 기본 골격"만 다룬다. `/checkout` 페이지의 Address Details, Review Your Order 등
화면 구성요소는 `page-ui.md` TC-PAGE-UI-034~041 범위이며 Phase 7(page-ui)에서 확장 예정이므로
이 Task에서는 만들지 않는다.

Locator 확정 근거(Playwright MCP 실측, 2026-08-31, https://automationexercise.com/view_cart,
로그아웃 상태, 장바구니에 상품 1개 담긴 상태에서 "Proceed To Checkout" 버튼 클릭):
- 로그인 요구 모달은 "Proceed To Checkout" 버튼 클릭 시 Cart 페이지(`/view_cart`) 위에
  노출되며(페이지 이동 없이 URL이 그대로 `/view_cart`로 유지됨을 `window.location.href`로
  확인), 컨테이너는 `id="checkoutModal"`로 페이지 전체 기준
  `document.querySelectorAll('#checkoutModal').length === 1`을 확인했다(6.1절 1순위 id
  적용). "Add to Cart" 확인 모달(`#cartModal`, `add_to_cart_modal.py`)과는 별개의 컨테이너다.
- 모달 내부 구조(`#checkoutModal` 기준 상대 CSS Selector, 각각 스코프 내 개수로 고유성 확인):
  - `.icon-box`(1개) - 상단 아이콘 컨테이너("사람 아이콘", TC-CART-010 Expected Result).
  - `.modal-title`(1개) - 텍스트 "Checkout".
  - `.modal-body`(1개) - 안내 문구("Register / Login account to proceed on checkout.")와
    "Register / Login" 링크를 감싼 문단 2개를 포함하는 컨테이너. `#cartModal`과 달리 이
    모달은 두 문단의 텍스트를 조합해 확인해도 TC 판정에 지장이 없어(안내 문구와 링크 텍스트가
    서로 다른 문자열이라 부분 문자열 포함 여부로 판정 가능) 별도로 `:first-of-type`까지
    좁히지 않고 컨테이너 전체 텍스트를 조회하는 `get_body_message_text()`를 제공한다.
  - `.modal-body a[href='/login']`(1개) - "Register / Login" 링크.
  - `.close-checkout-modal`(1개) - "Continue On Cart" 버튼(`data-dismiss="modal"`). 텍스트
    "Continue On Cart", `background-color: rgb(130, 206, 52)`(초록색, TC-CART-010 Expected
    Result "하단 초록색 'Continue On Cart' 버튼"과 일치)를 확인했다.
- "Continue On Cart" 클릭 시 모달만 닫히고(`data-dismiss="modal"`) 페이지 이동은 발생하지
  않음을 확인했다(`<button>` 요소, `click()` 그대로 사용).
- "Register / Login" 링크(`<a href="/login">`)는 실제 페이지 전체 이동을 트리거하므로
  `click_and_retry_if_vignette()`를 사용한다(다른 Page Object의 페이지 이동 링크와 동일 패턴).
- `/checkout` URL 자체는 로그아웃 상태에서 직접 접근해도 서버가 페이지를 렌더링함(Address
  Details가 비어있는 골격 상태)을 확인했으나, Approved TC(TC-CART-010/011)는 "Proceed To
  Checkout" 버튼 클릭이라는 트리거를 통한 진입만 다루므로 이 Page Object는 별도의
  `navigate()`를 제공하지 않는다(진입은 `CartPage.click_proceed_to_checkout()`이 담당).
  로그인 상태에서 버튼 클릭 시 모달 없이 `/checkout`으로 바로 이동하는지(TC-CART-011)는
  `BasePage.wait_for_url_contains("/checkout")`로 확인한다(이 Page Object에 별도 메서드를
  추가하지 않음 - 이미 BasePage가 제공).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """로그인 요구 모달(id="checkoutModal")의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/click_and_retry_if_vignette/get_text/get_css_value/is_element_visible)만
    사용해 요소를 조작·조회한다.
    """

    LOGIN_REQUIRED_MODAL = (By.ID, "checkoutModal")
    ICON_BOX = (By.CSS_SELECTOR, "#checkoutModal .icon-box")
    TITLE = (By.CSS_SELECTOR, "#checkoutModal .modal-title")
    BODY_MESSAGE = (By.CSS_SELECTOR, "#checkoutModal .modal-body")
    REGISTER_LOGIN_LINK = (By.CSS_SELECTOR, "#checkoutModal .modal-body a[href='/login']")
    CONTINUE_ON_CART_BUTTON = (By.CSS_SELECTOR, "#checkoutModal .close-checkout-modal")

    def is_login_required_modal_visible(self) -> bool:
        """로그인 요구 모달의 노출 여부를 반환한다."""
        return self.is_element_visible(self.LOGIN_REQUIRED_MODAL)

    def get_title_text(self) -> str:
        """모달 제목("Checkout") 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.TITLE)

    def get_body_message_text(self) -> str:
        """모달 본문(안내 문구 + "Register / Login" 링크 텍스트 포함) 전체 텍스트를 조회해
        반환한다(Assertion 없음)."""
        return self.get_text(self.BODY_MESSAGE)

    def get_register_login_link_text(self) -> str:
        """"Register / Login" 링크 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.REGISTER_LOGIN_LINK)

    def click_register_login(self) -> None:
        """"Register / Login" 링크를 클릭해 로그인 페이지(`/login`)로 이동한다.

        실제 페이지 전체 이동(`<a href="/login">`)을 트리거하므로
        `click_and_retry_if_vignette()`를 사용한다(위 docstring 참고).
        """
        self.click_and_retry_if_vignette(self.REGISTER_LOGIN_LINK)

    def get_continue_on_cart_button_text(self) -> str:
        """"Continue On Cart" 버튼 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.CONTINUE_ON_CART_BUTTON)

    def get_continue_on_cart_button_background_color(self) -> str:
        """"Continue On Cart" 버튼의 배경색(`background-color`)을 조회해 반환한다
        (Assertion 없음)."""
        return self.get_css_value(self.CONTINUE_ON_CART_BUTTON, "background-color")

    def click_continue_on_cart(self) -> None:
        """"Continue On Cart" 버튼을 클릭해 모달을 닫는다(Cart 페이지에 그대로 남음).

        `data-dismiss="modal"` 버튼으로 페이지 이동을 트리거하지 않으므로 일반 `click()`을
        사용한다.
        """
        self.click(self.CONTINUE_ON_CART_BUTTON)
