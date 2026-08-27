"""pytest 공통 fixture 정의.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md 9절 Fixture 원칙
- WebDriver 생성/종료는 여기서 fixture로 관리하며, yield 패턴으로 테스트 종료 후
  리소스 정리(driver.quit())를 보장한다.
- 기본 scope는 function으로 설정해 테스트마다 새 WebDriver를 생성한다(10절 테스트 독립성).
"""

import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """테스트마다 새로 생성/종료되는 Chrome WebDriver fixture."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
