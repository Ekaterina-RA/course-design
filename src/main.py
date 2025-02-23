import os
import pandas as pd
from config import DATA_DIR, file_path
from src.reports import spending_by_category, transactions_df
from src.services import get_beneficial_cashback_categories

operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
all_operations = pd.read_excel('operations.xlsx')
all_operations_list_dict = all_operations.to.dict(orient='records')

# Вызов функции "Функция «Выгодные категории повышенного кешбэка»

transactions = [
    {'date': '2023-10-01', 'amount': -1500, 'category': 'Еда'},
    {'date': '2023-10-05', 'amount': -2000, 'category': 'Транспорт'},
     {'date': '2023-10-10', 'amount': -3000, 'category': 'Наличные'},
    {'date': '2023-10-12', 'amount': -1000, 'category': 'Развлечения'},
    {'date': '2023-09-15', 'amount': -500, 'category': 'Еда'},
]
result = get_beneficial_cashback_categories(transactions, 2023, 10)
print(result)

