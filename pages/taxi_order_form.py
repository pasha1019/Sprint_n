"""Форма заказа такси: тарифы, тултипы и поля ввода."""

import re

from locators.taxi_order_form_locators import TaxiOrderFormLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage

TOOLTIP_HOVER_JS = """
    const btn = document.querySelector('.tariff-picker .tcard:nth-child(%(nth)d) .tcard-i');
    btn.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
    btn.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
"""

TOOLTIP_SHOWN_JS = """
    const t = document.getElementById('tariff-card-%(index)d');
    return t !== null
        && (t.classList.contains('show') || getComputedStyle(t).visibility === 'visible');
"""

TOOLTIP_TEXT_JS = """
    const t = document.getElementById('tariff-card-%(index)d');
    if (t === null) return '';
    t.querySelectorAll('span[style], div[style]').forEach(e => e.remove());
    return t.textContent;
"""


class TaxiOrderForm(BasePage):
    """Форма заказа такси, открывающаяся после выбора вида маршрута «Быстрый»."""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Сохраняет драйвер, базовый URL и локаторы формы заказа."""
        super().__init__(driver, base_url)
        self.locators = TaxiOrderFormLocators()

    def wait_shown(self, timeout: int = 30) -> None:
        """Ожидает появления формы заказа такси с выбором тарифа."""
        self.find_visible(self.locators.FORM_SHOWN, timeout=timeout)

    def tariff_count(self) -> int:
        """Возвращает количество карточек тарифов в форме заказа."""
        return len(self.find_all(self.locators.TARIFF_CARD))

    def tariff_titles(self) -> list[str]:
        """Возвращает названия всех тарифов в порядке отображения."""
        return [element.text for element in self.find_all(self.locators.TARIFF_TITLE_ALL)]

    def active_tariff_titles(self) -> list[str]:
        """Возвращает названия активных тарифов (ожидается один)."""
        return [element.text for element in self.find_all(self.locators.TARIFF_ACTIVE_TITLE)]

    def select_tariff(self, title: str) -> None:
        """Выбирает тариф по названию в форме заказа."""
        locator = (By.XPATH, self.locators.TARIFF_SELECT_TPL.format(title=title))
        self.find(locator).click()

    def active_tariff_price_text(self) -> str:
        """Возвращает цену активного тарифа."""
        return self.find_visible(self.locators.TARIFF_ACTIVE_PRICE).text

    def hover_tariff_info(self, index: int) -> None:
        """Наводит на иконку i тарифа с нулевым индексом.

        Тултип в React запускается событиями mouseenter/mouseover; JS-диспатч
        надёжнее ActionChains, т.к. тот на части карточек падает с
        ElementNotInteractableException («has no size and location»).
        """
        self.js(TOOLTIP_HOVER_JS % {"nth": index + 1})

    def is_tariff_tooltip_shown(self, index: int) -> bool:
        """Проверяет, отображается ли тултип тарифа с нулевым индексом."""
        return bool(self.js(TOOLTIP_SHOWN_JS % {"index": index}))

    def wait_tariff_tooltip_shown(self, index: int, timeout: int = 5) -> None:
        """Ожидает отображения тултипа тарифа с нулевым индексом."""
        WebDriverWait(self.driver, timeout).until(lambda _: self.is_tariff_tooltip_shown(index))

    def tariff_tooltip_text(self, index: int) -> str:
        """Возвращает текст тултипа тарифа с нулевым индексом без CSS-стилей."""
        text = self.js(TOOLTIP_TEXT_JS % {"index": index})
        return re.sub(r"\s+", " ", str(text)).strip()

    def phone_button_text(self) -> str:
        """Возвращает текст поля «Телефон» в форме заказа."""
        return self.find_visible(self.locators.PHONE_BUTTON).text

    def payment_button_text(self) -> str:
        """Возвращает текст поля «Способ оплаты» со значением в форме заказа."""
        return self.find_visible(self.locators.PAYMENT_BUTTON).text

    def comment_label_text(self) -> str:
        """Возвращает подпись поля «Комментарий водителю» в форме заказа."""
        return self.find_visible(self.locators.COMMENT_LABEL).text

    def is_comment_field_displayed(self) -> bool:
        """Проверяет, что поле ввода комментария отображается в форме заказа."""
        return bool(self.find_visible(self.locators.COMMENT_INPUT).is_displayed())

    def requirements_text(self) -> str:
        """Возвращает заголовок блока «Требования к заказу»."""
        return self.find_visible(self.locators.REQUIREMENTS).text

    def smart_button_text(self) -> str:
        """Возвращает текст кнопки оформления заказа в форме заказа."""
        return self.find_visible(self.locators.SMART_BUTTON).text

    def is_laptop_table_enabled(self) -> bool:
        """Проверяет, что переключатель «Столик для ноутбука» включён."""
        return bool(self.find(self.locators.LAPTOP_TABLE_INPUT).is_selected())

    def enable_laptop_table(self) -> None:
        """Включает переключатель «Столик для ноутбука» в требованиях к заказу.

        Блок требований свёрнут, поэтому сначала раскрывается его заголовок,
        затем ожидается видимость переключателя и он включается.
        """
        self.find(self.locators.REQS_HEADER).click()
        switch = self.find(self.locators.LAPTOP_TABLE_SWITCH)
        WebDriverWait(self.driver, 10).until(
            lambda _: switch.is_displayed() and switch.size["width"] > 0
        )
        switch.click()
        WebDriverWait(self.driver, 10).until(lambda _: self.is_laptop_table_enabled())

    def click_smart_button(self) -> None:
        """Нажимает кнопку «Ввести номер и заказать»."""
        self.find_visible(self.locators.SMART_BUTTON).click()
