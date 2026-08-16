"""Виджет карты: ожидание, чтение и проверка точек маршрута."""

from typing import Any

from locators.map_widget_locators import MapWidgetLocators
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage

ROUTE_PIN_COUNT_JS = """
    const pins = Array.from(document.querySelectorAll('#map [class*="route-pin"]'))
        .filter(e => Array.from(e.classList).some(c => c.endsWith('route-pin')));
"""


class MapWidget(BasePage):
    """Методы работы с картой маршрута."""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Сохраняет драйвер, базовый URL и локаторы карты."""
        super().__init__(driver, base_url)
        self.locators = MapWidgetLocators()

    def wait_for_route_points(self, expected: int = 2, timeout: int = 45) -> None:
        """Ожидает появления `expected` точек маршрута на карте.

        Ожидание реализовано через setTimeout в консоли браузера, т.к. маршрут
        отрисовывается асинхронно (multiRouter + геокодирование).
        """
        result = self.driver.execute_async_script(
            """
            const done = arguments[arguments.length - 1];
            const expected = %(expected)d;
            const deadline = Date.now() + %(timeout)d;
            (function check() {
                %(pins)s
                if (pins.length === expected) { done(pins.length); return; }
                if (Date.now() > deadline) { done(-1); return; }
                setTimeout(check, 250);
            })();
            """
            % {
                "expected": expected,
                "timeout": timeout * 1000,
                "pins": ROUTE_PIN_COUNT_JS,
            }
        )
        if result != expected:
            raise TimeoutError(
                f"Точки маршрута не появились: ожидалось {expected}, найдено {result}"
            )

    def route_points(self) -> list[dict[str, Any]]:
        """Возвращает данные точек маршрута (координаты, подпись, видимость)."""
        points = self.js(
            """
            const map = document.querySelector('#map');
            const mapRect = map.getBoundingClientRect();
            %(pins)s
            return pins.map(p => {
                const r = p.getBoundingClientRect();
                return {
                    x: Math.round(r.x + r.width / 2),
                    y: Math.round(r.y + r.height / 2),
                    text: (p.textContent || '').trim(),
                    visible: r.top >= mapRect.top && r.bottom <= mapRect.bottom
                              && r.left >= mapRect.left && r.right <= mapRect.right
                };
            });
            """
            % {"pins": ROUTE_PIN_COUNT_JS}
        )
        return points if isinstance(points, list) else []

    def route_point_elements(self) -> list[Any]:
        """Возвращает DOM-элементы точек маршрута."""
        elements = self.js(
            """
            %(pins)s
            return pins;
            """
            % {"pins": ROUTE_PIN_COUNT_JS}
        )
        return elements if isinstance(elements, list) else []

    def hover_route_points(self) -> None:
        """Наводит курсор на каждую точку маршрута для отображения подписей."""
        for element in self.route_point_elements():
            self.hover_element(element)

    def map_rect(self) -> dict[str, Any]:
        """Возвращает границы карты в координатах вьюпорта."""
        rect = self.js(
            """
            const r = document.querySelector('#map').getBoundingClientRect();
            return {
                x: Math.round(r.x),
                y: Math.round(r.y),
                w: Math.round(r.width),
                h: Math.round(r.height)
            };
            """
        )
        return rect if isinstance(rect, dict) else {}
