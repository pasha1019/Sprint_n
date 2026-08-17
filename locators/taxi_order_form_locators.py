"""Локаторы формы заказа такси с выбором тарифа."""

from selenium.webdriver.common.by import By


class TaxiOrderFormLocators:
    """Локаторы формы заказа: тарифы, тултипы и поля ввода."""

    FORM_SHOWN = (By.CSS_SELECTOR, ".tariff-picker.shown")
    TARIFF_CARD = (By.CSS_SELECTOR, ".tariff-picker .tcard")
    TARIFF_TITLE_ALL = (By.CSS_SELECTOR, ".tariff-picker .tcard .tcard-title")
    TARIFF_ACTIVE_TITLE = (By.CSS_SELECTOR, ".tariff-picker .tcard.active .tcard-title")
    TARIFF_ACTIVE_PRICE = (By.CSS_SELECTOR, ".tariff-picker .tcard.active .tcard-price")
    TARIFF_SELECT_TPL = (
        "//div[contains(@class, 'tcard')]"
        "[.//div[contains(@class, 'tcard-title') and text()='{title}']]"
    )
    TARIFF_I_BUTTON_TPL = ".tariff-picker .tcard:nth-child({nth}) .tcard-i"
    TOOLTIP_TPL = "#tariff-card-{index}"
    PHONE_BUTTON = (By.CSS_SELECTOR, ".np-button .np-text")
    PAYMENT_BUTTON = (By.CSS_SELECTOR, ".pp-button")
    COMMENT_INPUT = (By.CSS_SELECTOR, "input#comment")
    COMMENT_LABEL = (By.CSS_SELECTOR, "label[for='comment']")
    REQUIREMENTS = (By.CSS_SELECTOR, ".reqs-head")
    REQS_HEADER = (By.CSS_SELECTOR, ".reqs-header")
    LAPTOP_TABLE_SWITCH = (By.CSS_SELECTOR, ".r-sw .switch")
    LAPTOP_TABLE_INPUT = (By.CSS_SELECTOR, ".r-sw .switch-input")
    SMART_BUTTON = (By.CSS_SELECTOR, ".smart-button")
