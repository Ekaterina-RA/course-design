import pytest
from unittest.mock import patch
import json
from datetime import datetime
from src.services import get_beneficial_cashback_categories


# Фикстура для генерации тестовых данных
@pytest.fixture
def sample_data():
    return [
        {'date': '2023-01-15', 'category': 'Еда', 'amount': -500},
        {'date': '2023-01-20', 'category': 'Транспорт', 'amount': -150},
        {'date': '2023-01-25', 'category': 'Еда', 'amount': -300},
        {'date': '2023-02-10', 'category': 'Развлечения', 'amount': -200},
        {'date': '2023-02-15', 'category': 'Еда', 'amount': -150}
    ]


# Тест для функции get_beneficial_cashback_categories
@patch('src.services.logger')  # Заменяем логгер на Mock
def test_get_beneficial_cashback_categories(sample_data, mock_logger):
    # Проверяем кэшбэк за январь
    result = get_beneficial_cashback_categories(sample_data, 2023, 1)

    expected_result = {
        'Еда': 8,  # 1% от 500 + 1% от 300
        'Транспорт': 1.5  # 1% от 150
    }

    assert json.loads(result) == expected_result  # Проверяем результат

    # Проверяем, что логирование вызвано
    mock_logger.info.assert_any_call("Начинается анализ категорий кешбэка за %d-%02d", 2023, 1)
    mock_logger.info.assert_any_call("Отфильтрованные транзакции: %s", [sample_data[0], sample_data[1], sample_data[2]])
    mock_logger.info.assert_any_call("Сумма cashback: %s", expected_result)


# Параметризованный тест для разных месяцев
@pytest.mark.parametrize("year, month, expected_cashback", [
    (2023, 1, {'Еда': 8, 'Транспорт': 1.5}),
    (2023, 2, {'Еда': 1.5, 'Развлечения': 2}),  # 1% от 200 + 1% от 150
])
@patch('src.services.logger')  # Заменяем логгер на Mock
def test_get_beneficial_cashback_categories_parametrized(sample_data, year, month, expected_cashback, mock_logger):
    result = get_beneficial_cashback_categories(sample_data, year, month)

    assert json.loads(result) == expected_cashback  # Проверяем результат

    # Проверяем, что логирование вызвано
    mock_logger.info.assert_any_call("Начинается анализ категорий кешбэка за %d-%02d", year, month)