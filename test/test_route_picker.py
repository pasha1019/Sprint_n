"""Проверки блока с выбором маршрута."""

import allure
import pytest
from data.addresses import DIFFERENT_ADDRESS_CASES, FROM_ADDRESS
from pages.route_page import RoutePage


@allure.feature("Маршрут")
@allure.story("Блок с выбором маршрута")
@allure.severity(allure.severity_level.CRITICAL)
class TestRoutePickerBlock:
    """Сценарий «Отрисовка блока с выбором маршрута»."""

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title(
        "Под блоком адресов отображается блок с выбором маршрута: {address_from} -> {address_to}"
    )
    def test_picker_block_shown_for_different_addresses(
        self, route_page: RoutePage, address_from: str, address_to: str
    ) -> None:
        with allure.step(f"Ввести в поле «Откуда» адрес: {address_from}"):
            route_page.fill_from(address_from)

        with allure.step(f"Ввести в поле «Куда» адрес: {address_to}"):
            route_page.fill_to(address_to)

        with allure.step("Дождаться появления блока с выбором маршрута"):
            route_page.wait_type_picker_shown(timeout=30)

        with allure.step("Проверить, что блок с выбором маршрута отображается"):
            assert route_page.is_type_picker_shown(), "Блок с выбором маршрута не отображается"

        with allure.step("Проверить, что в блоке отображается результат маршрута"):
            assert route_page.type_picker_result(), "В блоке не отображается результат маршрута"

        route_page.take_screenshot("Блок с выбором маршрута")

    @allure.title(
        "При одинаковых адресах отображается блок с текстом «Авто Бесплатно В пути 0 мин.»"
    )
    def test_picker_block_text_for_same_address(self, route_page: RoutePage) -> None:
        with allure.step(f"Ввести в поле «Откуда» адрес: {FROM_ADDRESS}"):
            route_page.fill_from(FROM_ADDRESS)

        with allure.step(f"Ввести в поле «Куда» тот же адрес: {FROM_ADDRESS}"):
            route_page.fill_to(FROM_ADDRESS)

        with allure.step("Дождаться появления блока с выбором маршрута"):
            route_page.wait_type_picker_shown(timeout=30)

        with allure.step("Проверить текст блока"):
            assert route_page.type_picker_result() == "Авто Бесплатно В пути 0 мин.", (
                f"Текст блока: «{route_page.type_picker_result()}»"
            )

        route_page.take_screenshot("Блок с выбором маршрута (одинаковые адреса)")
