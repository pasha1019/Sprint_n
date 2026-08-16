"""Локаторы элементов виджета карты."""

from selenium.webdriver.common.by import By


class MapWidgetLocators:
    """Локаторы элементов карты маршрута."""

    MAP = (By.ID, "map")
