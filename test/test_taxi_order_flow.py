"""Проверки оформления заказа такси: поиск машины, совершенный заказ, детали и отмена."""

import re

import allure
from data.addresses import FROM_ADDRESS, TO_ADDRESS
from pages.order_window import OrderWindow
from pages.route_page import RoutePage
from pages.taxi_order_form import TaxiOrderForm


@allure.feature("Маршрут")
@allure.story("Оформление заказа такси")
@allure.severity(allure.severity_level.CRITICAL)
class TestTaxiOrderFlow:
    """Сценарий: после выбора тарифа «Рабочий» и опции «Столик для ноутбука»
    оформляется заказ такси: окно поиска машины, совершенный заказ, стоимость
    поездки в деталях и закрытие окна кнопкой «Отмена»."""

    def _place_taxi_order(
        self,
        route_page: RoutePage,
        taxi_order_form: TaxiOrderForm,
        order_window: OrderWindow,
    ) -> str:
        """Оформляет заказ такси и возвращает цену выбранного тарифа."""
        route_page.fill_from(FROM_ADDRESS)
        route_page.fill_to(TO_ADDRESS)
        route_page.wait_type_picker_shown(timeout=30)
        route_page.select_mode("Быстрый")
        route_page.wait_active_mode("Быстрый")
        route_page.click_result_button()
        taxi_order_form.wait_shown(timeout=30)

        with allure.step("Выбрать тариф «Рабочий» и включить «Столик для ноутбука»"):
            taxi_order_form.select_tariff("Рабочий")
            taxi_order_form.enable_laptop_table()
            assert taxi_order_form.is_laptop_table_enabled(), (
                "Переключатель «Столик для ноутбука» не включился"
            )
            tariff_price = taxi_order_form.active_tariff_price_text()

        with allure.step("Нажать «Ввести номер и заказать»"):
            taxi_order_form.click_smart_button()
            order_window.wait_shown(timeout=30)

        return tariff_price

    @staticmethod
    def _digits(value: str) -> str:
        """Возвращает только цифры из строки для сравнения стоимости."""
        return re.sub(r"[^\d]", "", value)

    @allure.title(
        "Оформление заказа такси: окно поиска машины, совершенный заказ, "
        "стоимость в деталях и отмена"
    )
    def test_taxi_order_flow(
        self,
        route_page: RoutePage,
        taxi_order_form: TaxiOrderForm,
        order_window: OrderWindow,
    ) -> None:
        tariff_price = self._place_taxi_order(route_page, taxi_order_form, order_window)

        with allure.step("Проверить элементы окна ожидания машины"):
            assert order_window.header_title_text() == "Поиск машины", (
                f"Ожидался заголовок «Поиск машины», найдено «{order_window.header_title_text()}»"
            )
            assert re.fullmatch(r"\d{2}:\d{2}", order_window.timer_text()), (
                f"Таймер поиска машины не в формате MM:SS: «{order_window.timer_text()}»"
            )
            labels = order_window.order_button_labels()
            assert "Отменить" in labels, f"Нет кнопки «Отменить», найдено: {labels}"
            assert "Детали" in labels, f"Нет кнопки «Детали», найдено: {labels}"

        with allure.step("Дождаться окончания поиска и проверить окно заказа"):
            order_window.wait_timer_finished(timeout=45)
            assert re.fullmatch(r"\d+ мин\. и приедет", order_window.header_title_text()), (
                f"Ожидался заголовок «N мин. и приедет», "
                f"найдено «{order_window.header_title_text()}»"
            )
            assert order_window.car_number_text(), "Не указан номер машины"
            assert order_window.rating_text(), "Не указан рейтинг водителя"
            assert order_window.driver_name_text(), "Не указано имя водителя"
            labels = order_window.order_button_labels()
            assert "Отменить" in labels, f"Нет кнопки «Отменить», найдено: {labels}"
            assert "Детали" in labels, f"Нет кнопки «Детали», найдено: {labels}"
            order_window.take_screenshot("Окно совершенного заказа")

        with allure.step("Проверить стоимость поездки в блоке «Еще про поездку»"):
            order_window.click_order_button("Детали")
            order_window.wait_details_shown(timeout=10)
            trip_cost = order_window.trip_cost_text()
            assert trip_cost, "Блок «Еще про поездку» не содержит стоимость"
            assert self._digits(trip_cost) == self._digits(tariff_price), (
                f"Стоимость в деталях «{trip_cost}» не совпадает с ценой тарифа «{tariff_price}»"
            )
            order_window.take_screenshot("Детали поездки со стоимостью")

        with allure.step("Отменить заказ и проверить закрытие окна"):
            order_window.click_order_button("Отменить")
            order_window.wait_closed(timeout=10)
            assert not order_window.is_shown(), "Окно заказа не закрылось после «Отмена»"
