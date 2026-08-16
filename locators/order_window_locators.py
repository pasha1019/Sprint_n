"""Локаторы окна заказа такси: поиск машины и совершенный заказ."""

from selenium.webdriver.common.by import By


class OrderWindowLocators:
    """Локаторы окна заказа, появляющегося после оформления заказа такси."""

    ORDER_SHOWN = (By.CSS_SELECTOR, ".order.shown")
    HEADER_TITLE = (By.CSS_SELECTOR, ".order-header-title")
    TIMER = (By.CSS_SELECTOR, ".order-header-time")
    CAR_NUMBER = (By.CSS_SELECTOR, ".order-number .number")
    RATING = (By.CSS_SELECTOR, ".order-btn-rating")
    BTN_GROUP = (By.CSS_SELECTOR, ".order-btn-group")
    DETAILS_SHOWN = (By.CSS_SELECTOR, ".order-details.shown")
    DETAIL_ROW = (By.CSS_SELECTOR, ".order-details.shown .order-details-row")
    DETAIL_HEAD = (By.CSS_SELECTOR, ".o-d-h")
    DETAIL_SUB = (By.CSS_SELECTOR, ".o-d-sh")
