import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
import logging
from src.reports import spending_by_category

# Настройка логирования
logger = logging.getLogger(__name__)

# Фикстура для генерации тестовых данных
@pytest.fixture
def transactions_data():
    data = {
        'Дата операции': [
            datetime(2023, 1, 15),
            datetime(2023, 2, 15),
            datetime(2023, 3, 15),
            datetime(2023, 4, 15),
            datetime(2023, 5, 15),
        ],
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения', 'Еда'],
        'Сумма операции': [-100, -50, -200, -300, -150]
    }
    return pd.DataFrame(data)


# Тест для функции spending_by_category
def test_spending_by_category_no_data(transactions_data):
    # Проверяем расходы по категории "Недвижимость", которой нет в данных
    result = spending_by_category(transactions_data, 'Недвижимость')

    assert result['category'] == 'Недвижимость'
    assert result['total_expenses'] == 0
    assert 'date_from' in result
    assert 'date_to' in result


def test_spending_by_category_missing_category_column(transactions_data):
    transactions_data_missing_column = transactions_data.drop(columns=['Категория'])

    # Проверяем, если столбец 'Категория' отсутствует
    result = spending_by_category(transactions_data_missing_column, 'Еда')

    assert result == {}