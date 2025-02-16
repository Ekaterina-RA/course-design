import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import os
from config import file_path, file_path1


def get_data_range(date_str, data_range='M'):
    """Возвращает начальную и конечную даты для анализа."""
    date = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
    if data_range == 'W':
        start_date = date - timedelta(days=date.weekday())
        end_date = date
    elif data_range == 'M':
        start_date = date.replace(day=1)
        end_date = date
    elif data_range == 'Y':
        start_date = date.replace(month=1, day=1)
        end_date = date
    elif data_range == 'ALL':
        start_date = datetime(2021, 1, 1, 16,44, 00 )
        end_date = date
    else:
        raise ValueError("Некорректный диапазон данных.")

    return start_date, end_date


def get_currency_rates(currencies):
    rates = {}
    for currency in currencies:
        try:
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{currency}')
            response.raise_for_status()  # Эта строка проверяет ошибки HTTP
            rates[currency] = response.json().get('rates', {})
        except requests.RequestException as e:
            print(f"Ошибка при получении курса валюты {currency}: {e}")
            rates[currency] = {}  # Или можете задуматься о других fallback значениях
    return rates


def get_stock_prices(stocks):
    """Получает цены акций."""
    prices = {}
    for stock in stocks:
        response = requests.get(f'https://api.marketstack.com/v1{stock}')
        prices[stock] = response.json().get('price', None)
    return prices


def group_expenses(filtered_data):
    """Группирует расходы по категориям и возвращает основные категории."""
    expenses_by_category = (
        filtered_data[filtered_data['Сумма операции'] < 0]
        .groupby('Категория')['Сумма операции']
        .sum()
        .reset_index()
    )
    expenses_by_category['Сумма операции'] = expenses_by_category['Сумма операции'].round(0)

    top_expenses = expenses_by_category.nlargest(7, 'Сумма операции')
    other_expenses_sum = expenses_by_category.loc[
        ~expenses_by_category['Категория'].isin(top_expenses['Категория']),
        'Сумма операции'
    ].sum()

    other_expenses = pd.DataFrame({'Категория': ['Остальное'], 'Сумма операции': [other_expenses_sum]})
    combined_expenses = pd.concat([top_expenses, other_expenses], ignore_index=True)

    return combined_expenses

def group_income(filtered_data):
    """Группирует поступления по категориям и возвращает основные категории."""
    income_by_category = (
        filtered_data[filtered_data['Сумма операции'] > 0]
        .groupby('Категория')['Сумма операции']
        .sum()
        .reset_index()
    )
    income_by_category['Сумма операции'] = income_by_category['Сумма операции'].round(0)
    top_income = income_by_category.nlargest(7, 'Сумма операции')
    other_income_sum = income_by_category.loc[
        ~income_by_category['Категория'].isin(top_income['Категория']),
        'Сумма операции'
    ].sum()
    other_income = pd.DataFrame({'Категория': ['Остальное'], 'Сумма операции': [other_income_sum]})
    combined_income = pd.concat([top_income, other_income], ignore_index=True)

    return combined_income

def analyze_data(date_str, data_range='M'):
    """Основная функция для анализа данных."""
    start_date, end_date = get_data_range(date_str, data_range)
    filtered_data = pd.read_excel(file_path)
    filtered_data['Дата операции'] = filtered_data['Дата операции'].astype(str).str.strip()

    try:
        # Преобразуйте 'Дата операции' в формат даты и времени
        filtered_data['Дата операции'] = pd.to_datetime(filtered_data['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    except Exception as e:
        print(f"Ошибка при преобразовании дат: {e}")

    # Фильтрация данных по дате
    filtered_data = filtered_data[(filtered_data['Дата операции'] >= start_date) & (filtered_data['Дата операции'] <= end_date)]
    # Анализ расходов
    expenses_summary = group_expenses(filtered_data)
    total_expenses = filtered_data['Сумма операции'].sum()
    # Анализ поступлений
    income_summary = group_income(filtered_data)
    total_income = filtered_data['Сумма операции'][filtered_data['Сумма операции'] > 0].sum()
    # Получение валютных курсов и цен акций
    try:
        with open(file_path1) as f:
            user_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Ошибка при чтении файла настроек пользователя: {e}")

    currency_rates = get_currency_rates(user_settings['user_currencies'])
    stock_prices = get_stock_prices(user_settings['user_stocks'])
    # Формирование итогового ответа
    result = {
        "Расходы": {
            "Общая сумма": total_expenses,
            "Основные": expenses_summary.to_dict(orient='records')
        },
        "Поступления": {
            "Общая сумма": total_income,
            "Основные": income_summary.to_dict(orient='records')  # Предполагается, что вы реализовали эту функцию
        },
        "Курс валют": currency_rates,
        "Цены акций": stock_prices
    }
    return result


# Пример вызова функции
result = analyze_data(date_str='31.12.2021 16:44:00', data_range='M')
print(json.dumps(result, ensure_ascii=False, indent=4))