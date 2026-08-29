"""모든 Page 클래스가 상속하는 공통 기반 클래스.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md (4.1절/7절/13절/15절)
- Page Layer는 화면 조작/조회 메서드만 제공하며 Assertion을 수행하지 않는다.
- 대기(Wait)는 고정 시간 대기 대신 WebDriverWait + expected_conditions만 사용한다.
- 예외는 Selenium이 실제로 발생시키는 구체적 예외만 명시적으로 처리하고 로깅한다.
"""

import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT


class BasePage:
    """모든 Page Object가 상속하는 공통 기반 클래스.

    WebDriver 인스턴스 1개만 보유하며, 공통 요소 탐색/클릭/입력/Wait 래핑 메서드를
    제공한다. Assertion은 절대 수행하지 않으며(Test Layer 책임), 발생 가능한 구체적
    예외만 명시적으로 처리하고 로깅한다.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def click(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> None:
        """요소가 클릭 가능해질 때까지 대기한 뒤 클릭한다."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.info("요소 클릭 완료: %s", locator)
        except TimeoutException:
            self.logger.error("요소가 클릭 가능한 상태가 되지 않음(Timeout): %s", locator)
            raise
        except NoSuchElementException:
            self.logger.error("요소를 찾을 수 없음: %s", locator)
            raise

    def type_text(self, locator: tuple, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """요소가 보일 때까지 대기한 뒤 기존 값을 지우고 텍스트를 입력한다.

        비밀번호 등 민감정보 노출 방지를 위해 입력값 자체는 로깅하지 않고
        로케이터만 로깅한다.
        """
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
