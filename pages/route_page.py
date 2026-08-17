"""Page Object страницы построения маршрута."""

from locators.route_page_locators import RoutePageLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class RoutePage(BasePage):
    """Страница построения маршрута: поля адресов и блок с выбором маршрута."""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Сохраняет драйвер, базовый URL и локаторы страницы."""
        super().__init__(driver, base_url)
        self.locators = RoutePageLocators()

    def wait_loaded(self, timeout: int = 30) -> None:
        """Ожидает загрузки полей адресов и карты."""
        self.find_visible(self.locators.FROM_INPUT, timeout=timeout)
        self.find_visible(self.locators.TO_INPUT, timeout=timeout)
        self.find(self.locators.MAP, timeout=timeout)

    def fill_from(self, address: str) -> None:
        """Вводит адрес отправления в поле «Откуда»."""
        self._fill(self.locators.FROM_INPUT, address)

    def fill_to(self, address: str) -> None:
        """Вводит адрес назначения в поле «Куда»."""
        self._fill(self.locators.TO_INPUT, address)

    def clear_from(self) -> None:
        """Очищает поле «Откуда»."""
        self._clear(self.locators.FROM_INPUT)

    def clear_to(self) -> None:
        """Очищает поле «Куда»."""
        self._clear(self.locators.TO_INPUT)

    def is_type_picker_shown(self) -> bool:
        """Проверяет, отображается ли блок с выбором маршрута."""
        return bool(self.driver.find_elements(*self.locators.TYPE_PICKER_SHOWN))

    def wait_type_picker_shown(self, timeout: int = 30) -> WebElement:
        """Ожидает появления блока с выбором маршрута."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.locators.TYPE_PICKER_SHOWN)
        )

    def type_picker_price_text(self) -> str:
        """Возвращает текст с ценой в блоке с выбором маршрута."""
        return self.find_visible(self.locators.TYPE_PICKER_RESULT_TEXT).text

    def type_picker_duration_text(self) -> str:
        """Возвращает текст с длительностью в блоке с выбором маршрута."""
        return self.find_visible(self.locators.TYPE_PICKER_DURATION).text

    def type_picker_result(self) -> str:
        """Возвращает полный текст результата в блоке с выбором маршрута."""
        return f"{self.type_picker_price_text()} {self.type_picker_duration_text()}"

    def type_picker_result_settled(self, timeout: int = 30) -> str:
        """Ожидает стабилизации результата маршрута и возвращает его.

        Результат (цена и время) пересчитывается асинхронно после переключения
        вида маршрута; значение считается устоявшимся, когда два последовательных
        чтения совпали.
        """
        state: list[str] = [self.type_picker_result(), ""]

        def _settled(_: WebDriver) -> bool:
            current = self.type_picker_result()
            if current == state[0]:
                state[1] = current
                return True
            state[0] = current
            return False

        WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(_settled)
        return state[1]

    def select_mode(self, mode_name: str) -> None:
        """Переключает вид маршрута: Оптимальный, Быстрый или Свой."""
        locator = (By.XPATH, self.locators.MODE_SELECT_TPL.format(name=mode_name))
        self.find(locator).click()

    def active_mode_text(self) -> str:
        """Возвращает название активного вида маршрута."""
        return self.find_visible(self.locators.MODE_ACTIVE).text

    def wait_active_mode(self, mode_name: str, timeout: int = 30) -> None:
        """Ожидает, пока указанный вид маршрута станет активным."""
        WebDriverWait(self.driver, timeout).until(lambda _: self.active_mode_text() == mode_name)

    def transport_type_states(self) -> list[bool]:
        """Возвращает флаги активности каждого типа передвижения."""
        return [
            "disabled" not in (element.get_attribute("class") or "")
            for element in self.find_all(self.locators.TYPES_CONTAINER)
        ]

    def select_drive(self) -> None:
        """Выбирает тип передвижения «Драйв» в виде маршрута «Свой»."""
        self.find(self.locators.TYPE_DRIVE).click()

    def result_button(self) -> WebElement:
        """Возвращает кнопку заказа в блоке результата маршрута."""
        return self.find_visible(self.locators.RESULT_BUTTON)

    def result_button_text(self) -> str:
        """Возвращает текст кнопки заказа в блоке результата маршрута."""
        return self.result_button().text

    def result_button_enabled(self) -> bool:
        """Проверяет, что кнопка заказа активна (доступна для нажатия)."""
        return self.result_button().is_enabled()

    def click_result_button(self) -> None:
        """Нажимает кнопку заказа (например, «Вызвать такси») в блоке результата."""
        self.result_button().click()

    def wait_result_button_text(self, expected: str, timeout: int = 30) -> None:
        """Ожидает появления кнопки с указанным текстом в блоке результата."""
        WebDriverWait(self.driver, timeout).until(lambda _: self.result_button_text() == expected)

    def _fill(self, locator: tuple[str, str], value: str) -> None:
        """Вводит значение в поле."""
        self.find_visible(locator).send_keys(value)

    def _clear(self, locator: tuple[str, str]) -> None:
        """Очищает поле, выделяя его содержимое и удаляя его."""
        element = self.find_visible(locator)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
