"""Проверки отрисовки маршрута на карте."""

import allure
import pytest
from data.addresses import ADDRESS_CASES
from pages.map_widget import MapWidget
from pages.route_page import RoutePage


@allure.feature("Маршрут")
@allure.story("Отрисовка маршрута")
@allure.severity(allure.severity_level.CRITICAL)
class TestRouteRendering:
    """Сценарий: при вводе двух разных предустановленных адресов в поля
    «Откуда» и «Куда» на карте отображаются две точки начала и конца маршрута."""

    @pytest.mark.parametrize("address_from, address_to, street_from, street_to", ADDRESS_CASES)
    @allure.title("На карте отображаются две точки маршрута: {address_from} -> {address_to}")
    def test_two_route_points_displayed(
        self,
        route_page: RoutePage,
        map_widget: MapWidget,
        address_from: str,
        address_to: str,
        street_from: str,
        street_to: str,
    ) -> None:
        with allure.step(f"Ввести в поле «Откуда» адрес: {address_from}"):
            route_page.fill_from(address_from)

        with allure.step(f"Ввести в поле «Куда» адрес: {address_to}"):
            route_page.fill_to(address_to)

        route_page.take_screenshot("До построения маршрута")

        with allure.step("Дождаться появления двух точек маршрута на карте"):
            map_widget.wait_for_route_points(expected=2, timeout=45)

        points = map_widget.route_points()
        with allure.step("Проверить, что на карте ровно две точки"):
            assert len(points) == 2, f"Ожидалось 2 точки, найдено {len(points)}"

        route_page.take_screenshot("После построения маршрута")

    @pytest.mark.parametrize("address_from, address_to, street_from, street_to", ADDRESS_CASES)
    @allure.title("Точки начала и конца маршрута различны и отображаются в границах карты")
    def test_route_points_are_distinct_and_within_map(
        self,
        route_page: RoutePage,
        map_widget: MapWidget,
        address_from: str,
        address_to: str,
        street_from: str,
        street_to: str,
    ) -> None:
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        map_widget.wait_for_route_points(expected=2, timeout=45)

        points = map_widget.route_points()
        assert len(points) == 2

        with allure.step("Точки не совпадают (разные координаты)"):
            first, second = points
            distance = abs(first["x"] - second["x"]) + abs(first["y"] - second["y"])
            assert distance >= 20, f"Точки маршрута слишком близко или совпадают (delta={distance})"

        with allure.step("Обе точки находятся в границах карты"):
            map_rect = map_widget.map_rect()
            for point in points:
                assert point["visible"], (
                    f"Точка ({point['x']}, {point['y']}) вне видимой области карты {map_rect}"
                )

    @pytest.mark.parametrize("address_from, address_to, street_from, street_to", ADDRESS_CASES)
    @allure.title("Подписи точек маршрута соответствуют введённым адресам (hover)")
    def test_route_point_labels_match_addresses(
        self,
        route_page: RoutePage,
        map_widget: MapWidget,
        address_from: str,
        address_to: str,
        street_from: str,
        street_to: str,
    ) -> None:
        route_page.fill_from(address_from)
        route_page.fill_to(address_to)
        map_widget.wait_for_route_points(expected=2, timeout=45)

        points = map_widget.route_points()
        elements = map_widget.route_point_elements()
        assert len(points) == 2 and len(elements) == 2

        with allure.step("Навести курсор на каждую точку маршрута"):
            map_widget.hover_route_points()

        texts = [point["text"] for point in points]
        with allure.step("Проверить, что подписи точек содержат введённые адреса"):
            for street in (street_from, street_to):
                assert any(street.lower() in text.lower() for text in texts), (
                    f"Адрес «{street}» не найден в подписях точек: {texts}"
                )
