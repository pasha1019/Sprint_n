"""Проверки подготовки к заказу такси: виды маршрута, типы передвижения и кнопки заказа."""

import allure
import pytest
from data.addresses import DIFFERENT_ADDRESS_CASES
from pages.route_page import RoutePage


@allure.feature("Маршрут")
@allure.story("Подготовка к заказу такси")
@allure.severity(allure.severity_level.CRITICAL)
class TestTaxiOrderPreparation:
    """Сценарий: при вводе двух разных предустановленных адресов в поля
    «Откуда» и «Куда» проверяется блок с выбором маршрута перед заказом такси."""

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title(
        "Переключение между видами маршрута меняет активный таб и пересчитывает "
        "время и стоимость: {address_from} -> {address_to}"
    )
    def test_mode_switch_changes_active_tab_and_recalculates_route(
        self, route_page: RoutePage, address_from: str, address_to: str
    ) -> None:
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        route_page.wait_type_picker_shown(timeout=30)

        with allure.step("Переключить вид маршрута на «Оптимальный»"):
            route_page.select_mode("Оптимальный")
            route_page.wait_active_mode("Оптимальный")
        optimal_result = route_page.type_picker_result_settled(timeout=30)
        assert route_page.active_mode_text() == "Оптимальный"

        with allure.step("Переключить вид маршрута на «Быстрый»"):
            route_page.select_mode("Быстрый")
            route_page.wait_active_mode("Быстрый")
        fast_result = route_page.type_picker_result_settled(timeout=30)
        assert route_page.active_mode_text() == "Быстрый"

        with allure.step("Проверить, что время и стоимость пересчитались"):
            assert optimal_result != fast_result, (
                f"Результат не пересчитался при смене вида маршрута: "
                f"{optimal_result} == {fast_result}"
            )

        route_page.take_screenshot("Блок с выбором маршрута после переключения видов")

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title(
        "В виде маршрута «Свой» активируются все типы передвижения: {address_from} -> {address_to}"
    )
    def test_custom_mode_activates_all_transport_types(
        self, route_page: RoutePage, address_from: str, address_to: str
    ) -> None:
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        route_page.wait_type_picker_shown(timeout=30)

        with allure.step("Проверить, что до переключения типы передвижения заблокированы"):
            assert route_page.transport_type_states() == [False] * 6, (
                "Типы передвижения активны до выбора вида маршрута «Свой»"
            )

        with allure.step("Переключить вид маршрута на «Свой»"):
            route_page.select_mode("Свой")
            route_page.wait_active_mode("Свой")

        with allure.step("Проверить, что активный таб сменился на «Свой»"):
            assert route_page.active_mode_text() == "Свой"

        with allure.step(
            "Проверить, что все типы передвижения стали активными "
            "(Машина, Пешком, Такси, Велосипед, Самокат, Драйв)"
        ):
            assert route_page.transport_type_states() == [True] * 6, (
                "Не все типы передвижения активны в виде маршрута «Свой»"
            )

        route_page.take_screenshot("Вид маршрута «Свой» с активными типами передвижения")

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title(
        "В виде маршрута «Быстрый» активна кнопка «Вызвать такси»: {address_from} -> {address_to}"
    )
    def test_fast_mode_has_active_call_taxi_button(
        self, route_page: RoutePage, address_from: str, address_to: str
    ) -> None:
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        route_page.wait_type_picker_shown(timeout=30)

        with allure.step("Переключить вид маршрута на «Быстрый»"):
            route_page.select_mode("Быстрый")
            route_page.wait_active_mode("Быстрый")

        with allure.step("Проверить кнопку «Вызвать такси»"):
            route_page.wait_result_button_text("Вызвать такси")
            assert route_page.result_button_text() == "Вызвать такси", (
                f"Ожидалась кнопка «Вызвать такси», найдено «{route_page.result_button_text()}»"
            )
            assert route_page.result_button_enabled(), "Кнопка «Вызвать такси» неактивна"

        route_page.take_screenshot("Вид маршрута «Быстрый» с кнопкой «Вызвать такси»")

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title(
        "В виде маршрута «Свой» с типом «Драйв» активна кнопка «Забронировать»: "
        "{address_from} -> {address_to}"
    )
    def test_custom_mode_with_drive_has_active_booking_button(
        self, route_page: RoutePage, address_from: str, address_to: str
    ) -> None:
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        route_page.wait_type_picker_shown(timeout=30)

        with allure.step("Переключить вид маршрута на «Свой» и выбрать тип «Драйв»"):
            route_page.select_mode("Свой")
            route_page.wait_active_mode("Свой")
            route_page.select_drive()

        with allure.step("Проверить кнопку «Забронировать»"):
            route_page.wait_result_button_text("Забронировать")
            assert route_page.result_button_text() == "Забронировать", (
                f"Ожидалась кнопка «Забронировать», найдено «{route_page.result_button_text()}»"
            )
            assert route_page.result_button_enabled(), "Кнопка «Забронировать» неактивна"

        route_page.take_screenshot("Вид маршрута «Свой» с типом «Драйв» и кнопкой «Забронировать»")
