"""Локаторы элементов страницы построения маршрута."""

from selenium.webdriver.common.by import By


class RoutePageLocators:
    """Локаторы полей адресов и блока с выбором маршрута."""

    FROM_INPUT = (By.CSS_SELECTOR, "input#from")
    TO_INPUT = (By.CSS_SELECTOR, "input#to")
    MAP = (By.ID, "map")
    TYPE_PICKER_SHOWN = (By.CSS_SELECTOR, ".type-picker.shown")
    TYPE_PICKER_RESULT_TEXT = (By.CSS_SELECTOR, ".type-picker .text")
    TYPE_PICKER_DURATION = (By.CSS_SELECTOR, ".type-picker .duration")
    MODE_ACTIVE = (By.CSS_SELECTOR, ".modes-container .mode.active")
    MODE_SELECT_TPL = "//div[contains(@class, 'mode') and text()='{name}']"
    TYPES_CONTAINER = (By.CSS_SELECTOR, ".types-container .type")
    TYPE_DRIVE = (By.CSS_SELECTOR, ".types-container .type.drive")
    RESULT_BUTTON = (By.CSS_SELECTOR, ".results-text .button")
