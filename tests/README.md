# Сайт закрытых городов Росатома

## Структура проекта

```
tests/
├── app.py                          # Flask приложение
├── requirements.txt                # Зависимости Python
├── templates/                      # Jinja2 шаблоны
│   ├── base.html                  # Базовый шаблон
│   ├── header.html                # Шапка сайта
│   ├── footer.html                # Футер сайта
│   └── index.html                 # Главная страница
├── static/                         # Статические файлы
│   ├── css/
│   │   └── styles.css             # Стили
│   ├── js/
│   │   ├── map.js                 # Логика карты
│   │   └── theme.js               # Переключение темы
│   └── languages/                  # Переводы
│       ├── ru/
│       │   ├── cities.json        # Города на русском
│       │   └── translations.json  # Переводы интерфейса
│       └── en/
│           ├── cities.json        # Города на английском
│           └── translations.json  # Переводы интерфейса
```

## Установка и запуск

1. Установите зависимости:
```cmd/bash
cd tests
pip install -r requirements.txt
```

2. Запустите приложение:

**Windows:**
```bash
python app.py
```

**Linux/Mac:**
```bash
python app.py
```

3. Откройте в браузере: http://localhost:5000


