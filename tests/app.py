"""
Главный файл приложения Flask - Добрые дела Росатома

Этот файл:
- Инициализирует Flask приложение
- Регистрирует все Blueprint'ы (модули маршрутов)
- Настраивает конфигурацию

Структура проекта:
- decorators/: декораторы для проверки авторизации и ролей
- utils/: вспомогательные функции (работа с данными, переводами)
- routes/: маршруты приложения, разделенные по функционалу
  - auth.py: авторизация и регистрация
  - main.py: главная страница и публичные разделы
  - admin.py: панель администратора
  - moderator.py: панель модератора
  - organizer.py: панель организатора
  - api.py: API endpoints
"""

from flask import Flask
import os

# Создание приложения
app = Flask(__name__)
app.secret_key = 'rosatom_secret_key_2025'

# Создание папки для данных
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Импорт и регистрация Blueprint'ов
from routes.auth import auth_bp
from routes.main import main_bp
from routes.api import api_bp
from routes.admin import admin_bp

# Регистрация маршрутов
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)

# Импорт остальных маршрутов (если они созданы)
try:
    from routes.moderator import moderator_bp
    app.register_blueprint(moderator_bp)
except ImportError:
    pass

try:
    from routes.organizer import organizer_bp
    app.register_blueprint(organizer_bp)
except ImportError:
    pass

try:
    from routes.nko import nko_bp
    app.register_blueprint(nko_bp)
except ImportError:
    pass


if __name__ == '__main__':
    print("🚀 Запуск приложения 'Добрые дела Росатома'")
    print("📂 Структура модулей:")
    print("   - decorators/: проверка авторизации")
    print("   - utils/: работа с данными")
    print("   - routes/: маршруты приложения")
    print("\n✅ Сервер запущен: http://localhost:5000")
    app.run(debug=True)
