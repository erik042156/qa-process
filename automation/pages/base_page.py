"""모든 Page 클래스가 상속하는 공통 기반 클래스.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md (4.1절/7절/13절/15절)
- Page Layer는 화면 조작/조회 메서드만 제공하며 Assertion을 수행하지 않는다.
- 대기(Wait)는 고정 시간 대기 대신 WebDriverWait + expected_conditions만 사용한다.
- 예외는 Selenium이 실제로 발생시키는 구체적 예외만 명시적으로 처리하고 로깅한다.
"""

import logging

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT


class BasePage:
    """모든 Page Object가 상속하는 공통 기반 클래스.

    WebDriver 인스턴스 1개만 보유하며, 공통 요소 탐색/클릭/입력/Wait 래핑 메서드를
    제공한다. Assertion은 절대 수행하지 않으며(Test Layer 책임), 발생 가능한 구체적
    예외만 명시적으로 처리하고 로깅한다.
    """

    # automationexercise.com(Production)에 제3자(Google Ads) 네트워크가 페이지 진입 시
    # 무작위로 주입하는 전면 광고 오버레이(Google Vignette 등)의 "Close" 컨트롤.
    # 사용자가 실측 스크린샷(2026-08-30)으로 제보한 실제 노출 사례(오버레이 상단의
    # "Close" 텍스트)를 근거로 정의했다. 광고는 사이트 자체가 아닌 제3자가 매번 다른
    # 마크업으로 무작위 주입하므로 Playwright MCP로 사전에 결정적으로 재현·검증할 수
    # 없어(AUTOMATION_GUIDE 5절 절차의 명시적 예외), 화면에 노출되는 "Close" 텍스트를
    # 텍스트 결합 상대 XPath로 탐색하는 최선(best-effort) 방식을 사용한다.
    #
    # [2026-08-30 코드 리뷰 반영 시도 및 재수정] 코드 리뷰(finding #1/#4)에서 이 셀렉터가
    # 너무 광범위하고(사이트 자체의 정상 "Close" UI를 오검지할 위험) 매 호출마다 1.5초
    # 대기가 성능에 영향을 준다는 지적을 받아, 처음에는 "뷰포트의 80%를 덮는 Google Ads
    # iframe이 있을 때만" Close를 탐색하도록 게이팅했었다. 그러나 재검증(전체 회귀
    # 재실행) 결과 실제로 관찰된 방해성 오버레이(예: 화면 중앙의 광고 카드형 대화상자)가
    # 항상 뷰포트의 80%를 채우는 것은 아니어서(예: 실측 카드 크기 약 79%×65%), 이
    # 크기 기준 게이팅이 실제 오버레이를 놓쳐 5개 테스트가 연쇄 실패하는 회귀를
    # 유발했다(전체 회귀 재실행으로 재현·확인, 실패 스크린샷으로 원인 규명). 이에 따라
    # 크기 기반 iframe 게이팅은 제거하고, `driver.find_elements()`(복수형 - `find_element`
    # 단수형과 달리 없으면 즉시 빈 리스트를 반환하며 `WebDriverWait` 폴링을 하지 않음)로
    # "Close" 요소 자체가 DOM에 실제로 존재하는지 먼저 즉시 확인하는 방식으로
    # 되돌렸다. 이 세션에서 수십 차례의 페이지 스크린샷을 실측 검토한 결과 이 사이트
    # 자체(automationexercise.com)의 정상 UI에서 "Close"라는 정확한 텍스트를 가진
    # 요소는 한 번도 관찰되지 않았으므로(모두 제3자 광고), finding #1이 우려한 오검지
    # 위험은 이 사이트에서는 실증적으로 낮다고 판단해 정확성(실제 오버레이를 놓치지
    # 않는 것)을 우선했다. `find_elements()`는 없을 때 즉시(폴링 없이) 반환되므로
    # 광고가 없는 일반적인 경우의 성능 저하도 없다(finding #4 목표는 유지된다).
    AD_OVERLAY_CLOSE_BUTTON = (By.XPATH, "//*[normalize-space(text())='Close']")
    # Close 요소가 존재함을 확인한 뒤 실제로 클릭 가능해지기까지 걸리는 짧은 대기 시간.
    AD_OVERLAY_DISMISS_TIMEOUT = 1.5

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def _dismiss_ad_overlay_if_present(self) -> None:
        """광고 오버레이가 떠 있으면 "Close"를 클릭해 닫는다(2026-08-30 추가).

        페이지 진입 시 간헐적으로 노출되는 전면 광고 오버레이가 실제 클릭/입력을
        가로막는 사례가 확인되어, 본래 동작(click/type_text)을 시작하기 전에 먼저
        오버레이 존재 여부를 짧게 확인하고 있으면 닫는다. 광고 자체는 Project PRD
        "8. 기타 제약사항"에 따라 검증 대상이 아니므로 이 메서드는 Assertion을
        수행하지 않는다.

        `driver.find_elements()`(복수형)로 `AD_OVERLAY_CLOSE_BUTTON`이 현재 DOM에
        존재하는지 먼저 즉시 확인하고, 없으면(대부분의 경우) 폴링 없이 곧바로
        반환한다(성능 저하 없음). 존재할 때만 `WebDriverWait`으로 클릭 가능한
        상태가 될 때까지 짧게 기다린 뒤 클릭한다. (위 클래스 상수 주석에 이 설계로
        재수정하게 된 실측 경위가 기록되어 있다.)
        """
        if not self.driver.find_elements(*self.AD_OVERLAY_CLOSE_BUTTON):
            return
        try:
            close_button = WebDriverWait(
                self.driver, self.AD_OVERLAY_DISMISS_TIMEOUT
            ).until(EC.element_to_be_clickable(self.AD_OVERLAY_CLOSE_BUTTON))
            close_button.click()
            self.logger.info("페이지 진입 시 광고 오버레이 감지되어 Close 클릭으로 닫음")
        except TimeoutException:
            self.logger.debug(
                "Close 요소는 DOM에 있었으나 클릭 가능한 상태가 되지 않음(정상 진행)"
            )
        except ElementClickInterceptedException:
            self.logger.warning(
                "광고 오버레이 Close 버튼 클릭이 다른 요소에 가로채짐 - 무시하고 진행"
            )

    def click(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> None:
        """요소가 클릭 가능해질 때까지 대기한 뒤 클릭한다.

        광고 iframe 등 페이지에 동적으로 삽입되는 요소가 대상 요소를 가려 클릭이
        가로채이는 경우(ElementClickInterceptedException, 2026-08-30 Task 8 - signup
        페이지 "Create Account" 버튼이 하단 광고 iframe에 가려 클릭이 실패하는 문제를
        실제 pytest 실행으로 재현·확인) 대상 요소를 뷰포트 중앙으로 스크롤한 뒤 1회
        재시도한다. Google Vignette 전면 광고처럼 뷰포트 전체(100vw/100vh)를 덮는
        오버레이는 스크롤로도 회피되지 않음을 실제 pytest 재실행(2026-08-30)으로 추가
        확인했으므로, 스크롤 재시도도 다시 가로채이면 최종적으로 JavaScript로 대상
        요소에 click 이벤트를 직접 디스패치한다(오버레이의 시각적 위치와 무관하게 대상
        DOM 요소에만 이벤트가 전달되는 표준적인 우회 기법). 광고 배너 자체는 Project
        PRD "8. 기타 제약사항"에 따라 검증 대상이 아니므로, 무한 재시도 대신 최대 2회
        (스크롤+네이티브 클릭 → JS 클릭)의 결정적인 재시도로만 우회한다.

        클릭을 시도하기 전에 `_dismiss_ad_overlay_if_present()`로 페이지 진입 시
        노출되는 전면 광고 오버레이가 있으면 먼저 닫는다(2026-08-30 추가).
        """
        self._dismiss_ad_overlay_if_present()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            try:
                element.click()
            except ElementClickInterceptedException:
                self.logger.warning(
                    "다른 요소(광고 등)에 가려 클릭이 가로채짐, 화면 중앙으로 스크롤 후 재시도: %s",
                    locator,
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )
                try:
                    element.click()
                except ElementClickInterceptedException:
                    self.logger.warning(
                        "스크롤 후에도 클릭이 가로채짐(전면 광고 오버레이로 추정), "
                        "JavaScript로 클릭 이벤트 직접 디스패치: %s",
                        locator,
                    )
                    self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("요소 클릭 완료: %s", locator)
        except TimeoutException:
            self.logger.error("요소가 클릭 가능한 상태가 되지 않음(Timeout): %s", locator)
            raise
        except NoSuchElementException:
            self.logger.error("요소를 찾을 수 없음: %s", locator)
            raise

    def click_and_retry_if_vignette(
        self, locator: tuple, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """`click()`으로 클릭한 뒤, URL에 `google_vignette`가 남아있으면 1회 재클릭한다.

        [2026-08-30 코드 리뷰 반영, finding #3] "Continue" 버튼처럼 클릭이 실제 페이지
        이동(`<a href="...">`)을 트리거하는 경우, `click()`의 스크롤/JS 클릭 우회로도
        클릭 자체는 성공하지만 Google Vignette 전면 광고가 그 직후에 개입해 URL 끝에
        `#google_vignette`만 추가된 채 실제 이동은 되지 않는 현상이 확인되었다(2026-08-30
        Task 8/10, `AccountCreatedPage`/`AccountDeletedPage`의 `click_continue()`에서
        각각 독립적으로 동일한 재시도 로직을 구현했다가, 한쪽에 이 방어가 누락되어 실제
        회귀가 발생한 전례가 있다). 이 메서드로 두 Page Object의 중복 코드를 통합해
        AUTOMATION_GUIDE 19절("2회 이상 반복되는 코드는 공통 메서드로 분리") 원칙을
        따른다. 무한 재시도가 아니라 최대 1회만 재클릭한다.

        [2026-08-31 코드 리뷰 반영] 최초 구현은 `click()` 직후 곧바로
        `self.driver.current_url`을 읽어 판단했는데, 이는 `wait_for_url_to_be()`/
        `wait_for_url_contains()`의 독스트링이 이미 경고하는 "클릭이 트리거한
        리다이렉트가 아직 완료되지 않은 상태를 읽을 수 있음" 문제에 이 메서드
        자신도 노출되어 있었다(리다이렉트가 이 판단 시점 이후에 `#google_vignette`로
        정착하면 재시도가 발동하지 않아 광고 개입을 놓칠 수 있음). `WebDriverWait`으로
        짧게(`AD_OVERLAY_DISMISS_TIMEOUT`) `google_vignette`가 URL에 나타나는지
        기다려 판단하도록 수정했다 — 나타나지 않으면(대부분의 경우) `TimeoutException`을
        정상 경로로 간주하고 그대로 반환한다.
        """
        self.click(locator, timeout)
        try:
            WebDriverWait(self.driver, self.AD_OVERLAY_DISMISS_TIMEOUT).until(
                EC.url_contains("google_vignette")
            )
        except TimeoutException:
            return
        self.logger.warning(
            "클릭 후 Google Vignette 광고로 추정되는 오버레이가 감지되어 재클릭 "
            "시도: %s",
            self.driver.current_url,
        )
        self.click(locator, timeout)

    def type_text(self, locator: tuple, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """요소가 보일 때까지 대기한 뒤 기존 값을 지우고 텍스트를 입력한다.

        비밀번호 등 민감정보 노출 방지를 위해 입력값 자체는 로깅하지 않고
        로케이터만 로깅한다.

        입력을 시도하기 전에 `_dismiss_ad_overlay_if_present()`로 페이지 진입 시
        노출되는 전면 광고 오버레이가 있으면 먼저 닫는다(2026-08-30 추가). 새로
        진입한 화면의 첫 상호작용이 클릭이 아니라 입력인 경우(예: 상세 정보 입력
        페이지의 첫 필드 입력)에도 동일하게 보호하기 위함이다.
        """
        self._dismiss_ad_overlay_if_present()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
            self.logger.info("텍스트 입력 완료 (로케이터: %s)", locator)
        except TimeoutException:
            self.logger.error("요소가 보이는 상태가 되지 않음(Timeout): %s", locator)
            raise
        except NoSuchElementException:
            self.logger.error("요소를 찾을 수 없음: %s", locator)
            raise
        except ElementNotInteractableException:
            # 2026-08-30 코드 리뷰 반영(finding #2): _dismiss_ad_overlay_if_present()가
            # 오버레이의 Close 클릭에 실패(가로채임)해 오버레이가 그대로 남아있으면,
            # 대상 입력란이 여전히 가려진 채 상호작용 불가 상태일 수 있다. click()처럼
            # 스크롤/JS 우회를 시도하는 대신(입력 필드는 JS로 값을 직접 대입하면 실제
            # 사용자 입력과 다른 이벤트 흐름이 발생해 폼 검증에 영향을 줄 수 있으므로
            # 지양한다), 원인을 명확히 로깅하고 예외를 그대로 전파해 테스트가 왜
            # 실패했는지 진단 가능하게 한다(AUTOMATION_GUIDE 15절 "조용히 삼키지
            # 않는다").
            self.logger.error(
                "요소가 상호작용 불가능한 상태(다른 요소에 가려짐 등): %s", locator
            )
            raise

    def get_text(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> str:
        """요소가 보일 때까지 대기한 뒤 텍스트를 조회해 반환한다(Assertion 없음)."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            text = element.text
            self.logger.debug("텍스트 조회 완료: %s -> %s", locator, text)
            return text
        except TimeoutException:
            self.logger.error("요소가 보이는 상태가 되지 않음(Timeout): %s", locator)
            raise
        except NoSuchElementException:
            self.logger.error("요소를 찾을 수 없음: %s", locator)
            raise

    def is_element_visible(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """요소가 지정된 시간 내에 보이는지 여부를 True/False로 반환한다."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.debug("요소가 지정된 시간 내에 보이지 않음: %s", locator)
            return False

    def find_element(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """요소가 DOM에 존재할 때까지 대기한 뒤 WebElement를 반환한다."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error("요소가 존재하는 상태가 되지 않음(Timeout): %s", locator)
            raise
        except NoSuchElementException:
            self.logger.error("요소를 찾을 수 없음: %s", locator)
            raise

    def wait_for_url_to_be(self, url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """URL이 지정한 값과 정확히 일치할 때까지 대기한다.

        클릭 등으로 트리거되는 페이지 리다이렉트 직후 `driver.current_url`을 바로
        읽으면 리다이렉트가 아직 완료되지 않은 상태를 읽을 수 있으므로(Flaky 원인),
        URL 비교 전에 이 메서드로 리다이렉트 완료를 명시적으로 기다린다.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))
            self.logger.debug("URL이 기대값과 일치함: %s", url)
        except TimeoutException:
            self.logger.error(
                "URL이 지정된 시간 내에 기대값과 일치하지 않음(Timeout): %s", url
            )
            raise

    def wait_for_url_contains(self, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """URL에 지정한 문자열이 포함될 때까지 대기한다.

        클릭 등으로 트리거되는 페이지 리다이렉트 직후 `driver.current_url`을 바로
        읽으면 리다이렉트가 아직 완료되지 않은 상태를 읽을 수 있으므로(Flaky 원인),
        URL 비교 전에 이 메서드로 리다이렉트 완료를 명시적으로 기다린다.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
            self.logger.debug("URL에 기대 문자열이 포함됨: %s", text)
        except TimeoutException:
            self.logger.error(
                "URL에 지정된 시간 내에 기대 문자열이 포함되지 않음(Timeout): %s", text
            )
            raise
