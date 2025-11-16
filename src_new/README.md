# Добрые дела Росатома

Прототип многостраничного сайта для объединения НКО, волонтёров и координаторов в городах присутствия ГК Росатом.
```commandline
adminka - adminnaf@gmail.com 123456
moder - moderatornaf@gmail.com qweqwe
```
## Структура проекта

```
├── manage.py                          # Главный файл Flask приложения
├── req_src_new.txt                    # Зависимости Python
├── .env                               # Переменные окружения
├── data_from_env.py                   # Загрузка данных из .env
├── tesdb.py                           # Тестирование БД
│
├── databaseModules/                   # Модули работы с базой данных
│   ├── __init__.py
│   ├── db_conncetion_pool.py         # Пул соединений с БД
│   ├── classCreatorTables.py         # Создание таблиц
│   ├── classUsersDB.py               # Работа с пользователями
│   ├── classNkoDB.py                 # Работа с НКО
│   ├── classNewsDB.py                # Работа с новостями
│   ├── classEventsDB.py              # Работа с событиями
│   ├── classKnowelegesDB.py          # Работа с базой знаний
│   ├── classCityRegionDB.py          # Работа с городами и регионами
│   ├── classFavoriteUsersDB.py       # Работа с избранным
│   ├── classOrganizationDB.py        # Работа с организациями
│   ├── classSmallFuncsDB.py          # Вспомогательные функции БД
│   └── helpModules.py                # Вспомогательные модули
│
├── webModules/                        # Модули веб-логики
│   ├── __init__.py
│   ├── login_page.py                 # Страница входа
│   ├── registration_page.py          # Страница регистрации
│   ├── profile_page.py               # Страница профиля
│   ├── admin_checker.py              # Проверка прав администратора
│   ├── hash_password_usr.py          # Хеширование паролей
│   ├── upload_file_from_flask.py     # Загрузка файлов
│   │
│   ├── nkoModules/                   # Модули НКО
│   ├── newsModules/                  # Модули новостей
│   ├── eventsModules/                # Модули событий
│   ├── knowelegeModules/             # Модули базы знаний
│   ├── adminModules/                 # Модули администратора
│   └── moderatorModules/             # Модули модератора
│
├── templates/                         # HTML шаблоны
│   ├── index.html                    # Главная страница
│   ├── login.html                    # Вход
│   ├── register.html                 # Регистрация
│   ├── profile.html                  # Профиль пользователя
│   ├── favorites.html                # Избранное
│   ├── 404.html                      # Страница ошибки 404
│   │
│   ├── nko.html                      # Список НКО
│   ├── nko-detail.html               # Детальная страница НКО
│   ├── nko-add.html                  # Добавление НКО
│   ├── nko-list.html                 # Список НКО (альтернативный)
│   ├── nko-map.html                  # Карта НКО
│   │
│   ├── news.html                     # Лента новостей
│   ├── news-detail.html              # Детальная страница новости
│   │
│   ├── calendar.html                 # Календарь событий
│   │
│   ├── knowledge.html                # База знаний
│   ├── course-detail.html            # Детальная страница курса
│   ├── theme-detail.html             # Детальная страница темы
│   │
│   ├── components/                   # Компоненты
│   │   ├── header.html               # Шапка сайта
│   │   └── footer.html               # Подвал сайта
│   │
│   ├── admin/                        # Панель администратора
│   │   └── admin-panel.html
│   │
│   └── moderator/                    # Панель модератора
│       └── moderator-panel.html
│
└── static/                            # Статические файлы
    ├── css/
    │   └── rosatom-main.css          # Единый файл стилей
    │
    ├── js/
    │   └── script.js                 # JavaScript функции
    │
    └── file_dir/                     # Загруженные файлы
```

## Запуск проекта

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск Flask сервера
```bash
Вы должны быть в папке src_new
python manage.py
```

Откройте браузер и перейдите по адресу из консоли, пример - `http://127.0.0.1:5000`
