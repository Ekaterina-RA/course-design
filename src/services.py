from datetime import datetime

def get_best_cashback_categories(operations: list[dict], year, month):
    'отрезаем ненужные словари списка'

    for operation in operations:
        operations_dt = datetime.strptime(operation['Дата операции'], %d.%m.%Y %H:%M:%S')
        if operations_dt.year != year or operations_dt.month != month:
            continue
