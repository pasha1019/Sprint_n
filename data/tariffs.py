"""Статические тестовые данные: тарифы такси и их описания по ТЗ."""

from pytest import mark, param

TAXI_TARIFFS = (
    ("Рабочий", "Для деловых особ, которых отвлекают"),
    ("Сонный", "Для тех, кто не выспался"),
    ("Отпускной", "Если пришла пора отдохнуть"),
    ("Разговорчивый", "Если мысли не выходят из головы"),
    ("Утешительный", "Если хочется свернуться калачиком"),
    ("Глянцевый", "Если нужно блистать"),
)

SWAPPED_DESCRIPTION_TARIFFS = {"Сонный", "Разговорчивый"}

TAXI_TARIFF_CASES = []
for index, (title, description) in enumerate(TAXI_TARIFFS):
    marks = (
        mark.xfail(
            strict=True,
            reason="BUG-1: описания «Сонный» и «Разговорчивый» перепутаны в приложении",
        )
        if title in SWAPPED_DESCRIPTION_TARIFFS
        else ()
    )
    TAXI_TARIFF_CASES.append(param(index, title, description, id=title, marks=marks))
