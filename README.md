# Sprint_n
Автотесты для учебного сервиса «Яндекс.Маршруты»

## Стек
pytest + Selenium (Chrome) + Allure, Page Object Model.

## Установка
```bash
pip install -r requirements.txt
pip install -e ".[dev]"   # или: pip install ruff mypy
```

## Запуск тестов
```bash
python -m pytest
```

Опции: `--url https://...` — базовый URL, `--headed` — браузер с окном.

## Проверки качества
```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy pages locators data test conftest.py
```

## Отчёт Allure
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Структура
- `pages/` — Page Object (BasePage, RoutePage, MapWidget, TaxiOrderForm, OrderWindow)
- `locators/` — локаторы элементов отдельным пакетом
- `data/` — статические тестовые данные (адреса, тарифы такси, параметризация)
- `test/` — тесты по функциональности (сценарии «Отрисовка маршрута», «Блок с выбором маршрута», «Подготовка к заказу такси», «Заказ тарифа Такси», «Оформление заказа такси»)
- `conftest.py` — фикстуры (Chrome 1920×1080, headless, page objects), Allure-хуки, опции `--url`, `--headed`

## Известный баг (xfail strict)
- **BUG-1** — описания тарифов «Сонный» и «Разговорчивый» перепутаны в тултипах относительно ТЗ (test_taxi_tariff_order.py)
