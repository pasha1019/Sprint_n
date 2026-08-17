"""Фикстуры, опции командной строки и Allure-хуки для тестов."""

from collections.abc import Generator
from typing import Any, cast

import allure
import pytest
from pages.map_widget import MapWidget
from pages.order_window import OrderWindow
from pages.route_page import RoutePage
from pages.taxi_order_form import TaxiOrderForm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

DEFAULT_URL = "https://qa-routes.education-services.ru/"
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


def pytest_addoption(parser: pytest.Parser) -> None:
    """Регистрирует опции командной строки для запуска тестов."""
    parser.addoption(
        "--url",
        action="store",
        default=DEFAULT_URL,
        help="Базовый URL сервиса",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Запускать браузер с отображением окна (без headless)",
    )


@pytest.fixture(scope="function")
def base_url(request: pytest.FixtureRequest) -> str:
    """Возвращает базовый URL сервиса из опции --url."""
    return cast(str, request.config.getoption("--url"))


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    """Создаёт драйвер Chrome (headless) и закрывает его после теста."""
    options = Options()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    driver.implicitly_wait(0)
    driver.set_script_timeout(90)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def route_page(driver: WebDriver, base_url: str) -> RoutePage:
    """Открывает страницу маршрутов и дожидается её загрузки (предусловие)."""
    page = RoutePage(driver, base_url)
    page.open()
    page.wait_loaded()
    return page


@pytest.fixture(scope="function")
def map_widget(driver: WebDriver, base_url: str) -> MapWidget:
    """Возвращает виджет карты для проверки точек маршрута."""
    return MapWidget(driver, base_url)


@pytest.fixture(scope="function")
def taxi_order_form(driver: WebDriver, base_url: str) -> TaxiOrderForm:
    """Возвращает форму заказа такси для проверки тарифов и полей."""
    return TaxiOrderForm(driver, base_url)


@pytest.fixture(scope="function")
def order_window(driver: WebDriver, base_url: str) -> OrderWindow:
    """Возвращает окно заказа такси для проверки поиска машины и заказа."""
    return OrderWindow(driver, base_url)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[object]
) -> Generator[Any, Any, None]:
    """Прикрепляет скриншот и HTML страницы к отчёту Allure при падении теста."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        funcargs = cast("dict[str, object]", getattr(item, "funcargs", {}))
        driver = funcargs.get("driver")
        if driver is not None:
            try:
                allure.attach(
                    cast(WebDriver, driver).get_screenshot_as_png(),
                    name="Скриншот при падении теста",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    cast(WebDriver, driver).page_source,
                    name="HTML-код страницы",
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception:
                pass
