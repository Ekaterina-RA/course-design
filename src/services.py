import json
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_beneficial_cashback_categories(data, year, month):
    """ Функция «Выгодные категории повышенного кешбэка»"""
    logger.info("Начинается анализ категорий кешбэка за %d-%02d", year, month)

    # Фильтруем транзакции по году и месяцу
    filtered_transactions = list(filter(lambda x:
                                        datetime.strptime(x['date'], "%Y-%m-%d").year == year and
                                        datetime.strptime(x['date'], "%Y-%m-%d").month == month, data))

    logger.info("Отфильтрованные транзакции: %s", filtered_transactions)

    # Подсчитываем сумму для каждой категории
    category_cashback = {}
    for transaction in filtered_transactions:
        category = transaction['category']
        amount = abs(transaction['amount'])
        if category in category_cashback:
            category_cashback[category] += amount
        else:
            category_cashback[category] = amount

    # Формируем кэшбэк (1% от суммы)
    cashbacks = {category: round(amount * 0.01) for category, amount in category_cashback.items()}

    logger.info("Сумма cashback: %s", cashbacks)

    return json.dumps(cashbacks, ensure_ascii=False, indent=4)

transactions = [
    {'date': '2023-10-01', 'amount': -1500, 'category': 'Еда'},
    {'date': '2023-10-05', 'amount': -2000, 'category': 'Транспорт'},
     {'date': '2023-10-10', 'amount': -3000, 'category': 'Наличные'},
    {'date': '2023-10-12', 'amount': -1000, 'category': 'Развлечения'},
    {'date': '2023-09-15', 'amount': -500, 'category': 'Еда'},
]
result = get_beneficial_cashback_categories(transactions, 2023, 10)
print(result)
