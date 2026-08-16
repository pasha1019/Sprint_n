"""Окно заказа такси: поиск машины, совершенный заказ и детали поездки."""

from locators.order_window_locators import OrderWindowLocators
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage

DRIVER_NAME_JS = """
    const rating = document.querySelector('.order-btn-rating');
    if (rating === null) return '';
    const group = rating.closest('.order-btn-group');
    return group === null ? '' : (group.lastElementChild.textContent || '').trim();
"""


class OrderWindow(BasePage):
    """Окно заказа такси: ожидание машины и завершённый заказ."""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Сохраняет драйвер, базовый URL и локаторы окна заказа."""
        super().__init__(driver, base_url)
        self.locators = OrderWindowLocators()

    def wait_shown(self, timeout: int = 30) -> None:
        """Ожидает появления окна заказа такси."""
        self.find_visible(self.locators.ORDER_SHOWN, timeout=timeout)

    def is_shown(self) -> bool:
        """Проверяет, что окно заказа отображается."""
        return bool(self.driver.find_elements(*self.locators.ORDER_SHOWN))

    def wait_closed(self, timeout: int = 10) -> None:
        """Ожидает закрытия окна заказа."""
        WebDriverWait(self.driver, timeout).until(lambda _: not self.is_shown())

    def header_title_text(self) -> str:
        """Возвращает заголовок окна заказа («Поиск машины» или «N мин. и приедет»)."""
        return self.find_visible(self.locators.HEADER_TITLE).text

    def timer_text(self) -> str:
        """Возвращает текст таймера поиска машины (формат MM:SS)."""
        return self.find_visible(self.locators.TIMER).text

    def wait_timer_finished(self, timeout: int = 45) -> None:
        """Ожидает окончания таймера поиска машины и появления заказа."""
        WebDriverWait(self.driver, timeout).until(
            lambda _: not self.driver.find_elements(*self.locators.TIMER)
        )

    def car_number_text(self) -> str:
        """Возвращает номер машины в окне совершенного заказа."""
        return self.find_visible(self.locators.CAR_NUMBER).text

    def rating_text(self) -> str:
        """Возвращает рейтинг водителя в окне совершенного заказа."""
        return self.find_visible(self.locators.RATING).text

    def driver_name_text(self) -> str:
        """Возвращает имя водителя в окне совершенного заказа."""
        return str(self.js(DRIVER_NAME_JS)).strip()

    def order_button_labels(self) -> list[str]:
        """Возвращает подписи кнопок в окне заказа (например, «Отменить»)."""
        return [element.text for element in self.find_all(self.locators.BTN_GROUP)]

    def click_order_button(self, label: str) -> None:
        """Нажимает кнопку окна заказа по подписи (например, «Детали»)."""
        for group in self.find_all(self.locators.BTN_GROUP):
            if label in group.text:
                group.click()
                return
        raise ValueError(f"Кнопка «{label}» не найдена в окне заказа")

    def wait_details_shown(self, timeout: int = 10) -> None:
        """Ожидает раскрытия блока деталей поездки."""
        self.find_visible(self.locators.DETAILS_SHOWN, timeout=timeout)

    def trip_cost_text(self) -> str:
        """Возвращает стоимость из блока «Еще про поездку»."""
        for row in self.find_all(self.locators.DETAIL_ROW):
            if row.find_element(*self.locators.DETAIL_HEAD).text == "Еще про поездку":
                return row.find_element(*self.locators.DETAIL_SUB).text
        return ""
