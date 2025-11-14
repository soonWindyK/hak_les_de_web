"""
Функции для работы с данными (JSON файлы)

Содержит:
- load_data: загрузка данных из JSON файла
- save_data: сохранение данных в JSON файл
- load_translations: загрузка переводов
- load_cities: загрузка списка городов
"""

import json
import os

DATA_DIR = 'data'


def load_data(filename):
    """
    Загрузка данных из JSON файла.
    
    Параметры:
        filename (str): имя файла (например, 'users.json')
    
    Возвращает:
        list: список данных или пустой список, если файл не найден
    
    Пример:
        users = load_data('users.json')
    """
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_data(filename, data):
    """
    Сохранение данных в JSON файл.
    
    Параметры:
        filename (str): имя файла (например, 'users.json')
        data (list/dict): данные для сохранения
    
    Пример:
        save_data('users.json', users_list)
    """
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_translations(lang='ru'):
    """
    Загрузка переводов для указанного языка.
    
    Параметры:
        lang (str): код языка ('ru' или 'en')
    
    Возвращает:
        dict: словарь с переводами
    
    Пример:
        translations = load_translations('ru')
        print(translations['login'])  # "Войти"
    """
    translations_path = os.path.join('static', 'languages', lang, 'translations.json')
    with open(translations_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_cities(lang='ru'):
    """
    Загрузка списка городов для указанного языка.
    
    Параметры:
        lang (str): код языка ('ru' или 'en')
    
    Возвращает:
        list: список городов с координатами и информацией
    
    Пример:
        cities = load_cities('ru')
    """
    cities_path = os.path.join('static', 'languages', lang, 'cities.json')
    with open(cities_path, 'r', encoding='utf-8') as f:
        return json.load(f)
