"""Статические тестовые данные: предустановленные адреса сервиса маршрутов."""

from pytest import param

FROM_ADDRESS = "Хамовнический Вал, 34"
TO_ADDRESS = "Зубовский бульвар, 37"

STREET_FROM = "Хамовнический Вал"
STREET_TO = "Зубовский бульвар"

ADDRESS_CASES = [
    param(FROM_ADDRESS, TO_ADDRESS, STREET_FROM, STREET_TO, id="direct-order"),
    param(TO_ADDRESS, FROM_ADDRESS, STREET_TO, STREET_FROM, id="reverse-order"),
]

DIFFERENT_ADDRESS_CASES = [
    param(FROM_ADDRESS, TO_ADDRESS, id="direct-order"),
    param(TO_ADDRESS, FROM_ADDRESS, id="reverse-order"),
]
