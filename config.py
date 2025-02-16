import os
from logging import FileHandler

import pandas as pd

ROOT_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
file_path = os.path.join(DATA_DIR, 'operations.xlsx')
file_path1 = os.path.join(DATA_DIR, 'user_settings.json')

# Проверяем существование файла
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Файл не найден: {file_path}")

# Читаем данные из Excel
filtered_data = pd.read_excel(file_path)

operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
pd.read_excel(operations_path)

#FileHandler(os.path(LOGS_DIR, 'view.log')) - ПРИМЕР ПУТИ К ЛОГАМ