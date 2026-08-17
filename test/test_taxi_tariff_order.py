"""Проверки заказа тарифа такси: тарифы, тултипы и поля формы заказа."""

import allure
import pytest
from data.addresses import DIFFERENT_ADDRESS_CASES, FROM_ADDRESS, TO_ADDRESS
from data.tariffs import TAXI_TARIFF_CASES, TAXI_TARIFFS
from pages.route_page import RoutePage
from pages.taxi_order_form import TaxiOrderForm


@allure.feature("Маршрут")
@allure.story("Заказ тарифа Такси")
@allure.severity(allure.severity_level.CRITICAL)
class TestTaxiTariffOrder:
    """Сценарий: при вводе двух разных предустановленных адресов и выборе
    вида маршрута «Быстрый» открывается форма заказа такси с тарифами по ТЗ,
    тултипами при наведении на иконку i и блоком полей заказа."""

    def _open_taxi_order_form(
        self,
        route_page: RoutePage,
        taxi_order_form: TaxiOrderForm,
        address_from: str,
        address_to: str,
    ) -> None:
        """Открывает форму заказа такси: вводит адреса и выбирает «Быстрый»."""
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        route_page.wait_type_picker_shown(timeout=30)
        route_page.select_mode("Быстрый")
        route_page.wait_active_mode("Быстрый")
        route_page.click_result_button()
        taxi_order_form.wait_shown(timeout=30)

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title(
        "Форма заказа такси показывает 6 тарифов по ТЗ, один из них активный: "
        "{address_from} -> {address_to}"
    )
    def test_taxi_order_form_shows_six_tariffs_with_one_active(
        self,
        route_page: RoutePage,
        taxi_order_form: TaxiOrderForm,
        address_from: str,
        address_to: str,
    ) -> None:
        self._open_taxi_order_form(route_page, taxi_order_form, address_from, address_to)

        expected_titles = [title for title, _ in TAXI_TARIFFS]
        with allure.step("Проверить, что отображаются все 6 тарифов из ТЗ"):
            assert taxi_order_form.tariff_count() == 6, (
                f"Ожидалось 6 тарифов, найдено {taxi_order_form.tariff_count()}"
            )
            assert taxi_order_form.tariff_titles() == expected_titles, (
                f"Тарифы не соответствуют ТЗ: {taxi_order_form.tariff_titles()}"
            )

        with allure.step("Проверить, что ровно один тариф активен"):
            active = taxi_order_form.active_tariff_titles()
            assert len(active) == 1, f"Ожидался один активный тариф, найдено: {active}"
            assert active[0] in expected_titles, f"Активный тариф не из ТЗ: {active}"

        taxi_order_form.take_screenshot("Форма заказа такси с 6 тарифами")

    @pytest.mark.parametrize("tariff_index, tariff_title, tariff_description", TAXI_TARIFF_CASES)
    @allure.title("Тултип тарифа «{tariff_title}» при наведении на i показывает описание по ТЗ")
    def test_tariff_info_tooltip_matches_tz_description(
        self,
        route_page: RoutePage,
        taxi_order_form: TaxiOrderForm,
        tariff_index: int,
        tariff_title: str,
        tariff_description: str,
    ) -> None:
        self._open_taxi_order_form(route_page, taxi_order_form, FROM_ADDRESS, TO_ADDRESS)

        with allure.step(f"Навести на иконку i тарифа «{tariff_title}»"):
            taxi_order_form.hover_tariff_info(tariff_index)
            taxi_order_form.wait_tariff_tooltip_shown(tariff_index, timeout=5)

        with allure.step("Проверить, что тултип отображается и содержит описание по ТЗ"):
            assert taxi_order_form.is_tariff_tooltip_shown(tariff_index), (
                f"Тултип тарифа «{tariff_title}» не отображается"
            )
            tooltip_text = taxi_order_form.tariff_tooltip_text(tariff_index)
            assert tariff_description in tooltip_text, (
                f"Описание тарифа «{tariff_title}» не совпадает с ТЗ: "
                f"ожидалось «{tariff_description}», в тултипе «{tooltip_text}»"
            )

        taxi_order_form.take_screenshot(f"Тултип тарифа «{tariff_title}»")

    @pytest.mark.parametrize("address_from, address_to", DIFFERENT_ADDRESS_CASES)
    @allure.title("Под тарифами отображается блок полей заказа: {address_from} -> {address_to}")
    def test_taxi_order_form_fields_displayed(
        self,
        route_page: RoutePage,
        taxi_order_form: TaxiOrderForm,
        address_from: str,
        address_to: str,
    ) -> None:
        self._open_taxi_order_form(route_page, taxi_order_form, address_from, address_to)

        with allure.step("Проверить поле «Телефон»"):
            assert taxi_order_form.phone_button_text() == "Телефон", (
                f"Ожидалось «Телефон», найдено «{taxi_order_form.phone_button_text()}»"
            )

        with allure.step("Проверить поле «Способ оплаты» со значением «Наличные»"):
            payment = taxi_order_form.payment_button_text()
            assert "Способ оплаты" in payment, f"Не найдено «Способ оплаты» в «{payment}»"
            assert "Наличные" in payment, f"Не найдено «Наличные» в «{payment}»"

        with allure.step("Проверить поле «Комментарий водителю»"):
            comment_label = taxi_order_form.comment_label_text()
            assert "Комментарий водителю" in comment_label, (
                f"Ожидалась подпись «Комментарий водителю», найдено «{comment_label}»"
            )
            assert taxi_order_form.is_comment_field_displayed(), (
                "Поле ввода комментария не отображается"
            )

        with allure.step("Проверить блок «Требования к заказу»"):
            assert taxi_order_form.requirements_text() == "Требования к заказу", (
                f"Ожидался заголовок «Требования к заказу», "
                f"найдено «{taxi_order_form.requirements_text()}»"
            )

        with allure.step("Проверить кнопку «Ввести номер и заказать»"):
            smart_button = taxi_order_form.smart_button_text()
            assert "Ввести номер и заказать" in smart_button, (
                f"Ожидалась кнопка «Ввести номер и заказать», найдено «{smart_button}»"
            )

        taxi_order_form.take_screenshot("Блок полей формы заказа такси")
