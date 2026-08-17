"""Базовый Page Object с общими методами для всех страниц сервиса."""

from typing import Any

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовые операции со страницей: навигация, поиск элементов, скрипты."""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Сохраняет драйвер и базовый URL сервиса."""
        self.driver = driver
        self.base_url = base_url

    def open(self, path: str = "") -> None:
        """Открывает страницу по базовому URL с опциональным путём."""
        self.driver.get(self.base_url + path)

    def find(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """Возвращает элемент по локатору после появления в DOM."""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """Возвращает видимый элемент по локатору."""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: tuple[str, str], timeout: int = 10) -> list[WebElement]:
        """Возвращает список элементов по локатору после появления в DOM."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def js(self, script: str, *args: Any) -> Any:
        """Выполняет JavaScript-скрипт в контексте страницы."""
        return self.driver.execute_script(script, *args)

    def hover_element(self, element: WebElement) -> None:
        """Наводит курсор на элемент."""
        ActionChains(self.driver).move_to_element(element).perform()

    def take_screenshot(self, name: str) -> None:
        """Делает скриншот страницы и прикрепляет его к отчёту Allure."""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
