import pytest
from unittest.mock import patch
from datetime import datetime
import requests
import pandas as pd
from src.utils import get_data_range, get_currency_rates, get_stock_prices, group_expenses, group_income

# Тесты для функции get_data_range
@pytest.mark.parametrize("date_str, data_range, expected_start, expected_end", [
    ('01.01.2023', 'M', datetime(2023, 1, 1, 0, 0, 0), datetime(2023, 1, 31, 23, 59, 59)),
    ('01.01.2023', 'W', datetime(2022, 12, 26, 0, 0, 0), datetime(2023, 1, 1, 23, 59, 59)),  # Corrected expected dates
    ('01.01.2023', 'Y', datetime(2023, 1, 1, 0, 0, 0), datetime(2023, 12, 31, 23, 59, 59)),
    ('01.01.2023', 'ALL', datetime(2021, 1, 1, 16, 44, 0), datetime(2023, 1, 1, 0, 0, 0)),
])
def test_get_data_range(date_str, data_range, expected_start, expected_end):
    start, end = get_data_range(date_str, data_range)
    assert start == expected_start
    assert end == expected_end

    with pytest.raises(ValueError):
        get_data_range('01.01.2023', 'INVALID')


# Тесты для функции get_stock_prices
@patch('requests.get')
def test_get_stock_prices(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'price': 150
    }

    prices = get_stock_prices(['AAPL'])
    assert prices == {'AAPL': 150}  # Проверка результат

# Тесты для функции group_expenses
def test_group_expenses():
    data = pd.DataFrame({
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения'],
        'Сумма операции': [-50, -20, -30, -10]
    })

    result = group_expenses(data)
    assert result.shape[0] >= 4  # Проверка на количество уникальных категорий
    assert 'Остальное' in result['Категория'].values  # Проверяем, что 'Остальное' есть в результатах

# Тесты для функции group_income
def test_group_income():
    data = pd.DataFrame({
        'Категория': ['Зарплата', 'Инвестиции', 'Зарплата', 'Подарки'],
        'Сумма операции': [1000, 200, 500, 100]
    })

    result = group_income(data)
    assert result.shape[0] >= 4  # Проверка на количество уникальных категорий
    assert 'Остальное' in result['Категория'].values  # Проверяем, что 'Остальное' есть в результатах
    assert result['Категория'].iloc[0] == 'Зарплата'  # Проверяем, что 'Зарплата' в первой строке