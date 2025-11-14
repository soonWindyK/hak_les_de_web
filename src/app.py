from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os
import re
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'rosatom_secret_key_2025'

# Хранилище данных (вместо БД)
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Функция проверки email
def is_valid_email(email):
    """Проверка корректности email адреса"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Декоратор для проверки роли
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if session['user']['role'] not in roles:
                flash('У вас нет доступа к этой странице', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Загрузка переводов
def load_translations(lang='ru'):
    translations_path = os.path.join('static', 'languages', lang, 'translations.json')
    with open(translations_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Загрузка данных городов
def load_cities(lang='ru'):
    cities_path = os.path.join('static', 'languages', lang, 'cities.json')
    with open(cities_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Загрузка данных из JSON файлов
def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Главная страница
@app.route('/')
def index():
    lang = session.get('lang', 'ru')
    city = session.get('city', None)
    translations = load_translations(lang)
    return render_template('index.html', translations=translations, lang=lang, city=city)

# Список НКО
@app.route('/nko')
def nko_list():
    lang = session.get('lang', 'ru')
    city = request.args.get('city', session.get('city'))
    translations = load_translations(lang)
    nko_data = load_data('nko.json')
    
    # Фильтрация по городу
    if city:
        nko_data = [nko for nko in nko_data if nko.get('approved') and (nko.get('city') == city or not nko.get('city'))]
    else:
        nko_data = [nko for nko in nko_data if nko.get('approved')]
    
    return render_template('nko_list.html', translations=translations, lang=lang, nko_list=nko_data, city=city)

# Страница НКО
@app.route('/nko/<int:nko_id>')
def nko_detail(nko_id):
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    nko_data = load_data('nko.json')
    
    nko = next((n for n in nko_data if n['id'] == nko_id), None)
    if not nko:
        return "НКО не найдена", 404
    
    return render_template('nko_detail.html', translations=translations, lang=lang, nko=nko)

# База знаний
@app.route('/knowledge')
def knowledge():
    lang = session.get('lang', 'ru')
    category = request.args.get('category', 'all')
    translations = load_translations(lang)
    materials = load_data('knowledge.json')
    
    if category != 'all':
        materials = [m for m in materials if m.get('category') == category]
    
    return render_template('knowledge.html', translations=translations, lang=lang, materials=materials, category=category)

# Календарь событий
@app.route('/calendar')
def calendar():
    lang = session.get('lang', 'ru')
    city = request.args.get('city', session.get('city'))
    translations = load_translations(lang)
    events = load_data('events.json')
    
    # Показываем только одобренные события
    events = [e for e in events if e.get('approved', False)]
    
    if city:
        events = [e for e in events if e.get('city') == city or not e.get('city')]
    
    return render_template('calendar.html', translations=translations, lang=lang, events=events, city=city)

# Новости
@app.route('/news')
def news():
    lang = session.get('lang', 'ru')
    city = request.args.get('city', session.get('city'))
    translations = load_translations(lang)
    news_data = load_data('news.json')
    
    if city:
        news_data = [n for n in news_data if n.get('city') == city or not n.get('city')]
    
    return render_template('news.html', translations=translations, lang=lang, news_list=news_data, city=city)

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Проверка корректности email
        if not is_valid_email(email):
            flash('Некорректный формат email адреса', 'error')
            return render_template('login.html', translations=translations, lang=lang)
        
        users = load_data('users.json')
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        
        if user:
            session['user'] = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'city': user.get('city')
            }
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('login.html', translations=translations, lang=lang)

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)

    from src.flaskModules.registration_page import reg_page
    from src.databaseModules.classCityRegionDB import CityRegionDB_module

    if request.method == 'POST':
        return reg_page(request)

    cities_list = CityRegionDB_module().get_cities_list_with_region()
    print(cities_list)
    return render_template('register.html', translations=translations, lang=lang, cities_list=cities_list)

# Выход
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))

# Личный кабинет
@app.route('/profile')
@login_required
def profile():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    favorites = session.get('favorites', {'news': [], 'events': [], 'materials': []})
    
    # Перенаправление на соответствующую панель в зависимости от роли
    if user['role'] == 'admin':
        return redirect(url_for('admin_panel'))
    elif user['role'] == 'moderator':
        return redirect(url_for('moderator_panel'))
    elif user['role'] == 'organizer':
        return redirect(url_for('organizer_panel'))
    
    return render_template('profile.html', translations=translations, lang=lang, user=user, favorites=favorites)

# Панель модератора
@app.route('/moderator')
@role_required(['moderator', 'admin'])
def moderator_panel():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    # Загрузка данных для модерации
    pending_events = [e for e in load_data('events.json') if not e.get('approved', False)]
    pending_nko = [n for n in load_data('nko.json') if not n.get('approved', False)]
    
    return render_template('moderator_panel.html', 
                         translations=translations, 
                         lang=lang, 
                         user=user,
                         pending_events=pending_events,
                         pending_nko=pending_nko)

# Панель организатора
@app.route('/organizer')
@role_required(['organizer', 'moderator', 'admin'])
def organizer_panel():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    # Загрузка мероприятий организатора
    events = load_data('events.json')
    my_events = [e for e in events if e.get('organizer_id') == user['id']]
    
    return render_template('organizer_panel.html', 
                         translations=translations, 
                         lang=lang, 
                         user=user,
                         my_events=my_events)

# Создание мероприятия (организатор)
@app.route('/organizer/create-event', methods=['GET', 'POST'])
@role_required(['organizer', 'moderator', 'admin'])
def create_event():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    if request.method == 'POST':
        events = load_data('events.json')
        
        new_event = {
            'id': len(events) + 1,
            'title': request.form.get('title'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'location': request.form.get('location'),
            'city': request.form.get('city'),
            'description': request.form.get('description'),
            'organizer': user['name'],
            'organizer_id': user['id'],
            'approved': False,  # Требует модерации
            'created_at': datetime.now().isoformat()
        }
        
        events.append(new_event)
        save_data('events.json', events)
        
        flash('Мероприятие создано и отправлено на модерацию', 'success')
        return redirect(url_for('organizer_panel'))
    
    return render_template('create_event.html', translations=translations, lang=lang, user=user)

# Одобрение мероприятия (модератор)
@app.route('/moderator/approve-event/<int:event_id>', methods=['POST'])
@role_required(['moderator', 'admin'])
def approve_event(event_id):
    events = load_data('events.json')
    
    for event in events:
        if event['id'] == event_id:
            event['approved'] = True
            event['approved_at'] = datetime.now().isoformat()
            break
    
    save_data('events.json', events)
    flash('Мероприятие одобрено', 'success')
    return redirect(url_for('moderator_panel'))

# Отклонение мероприятия (модератор)
@app.route('/moderator/reject-event/<int:event_id>', methods=['POST'])
@role_required(['moderator', 'admin'])
def reject_event(event_id):
    events = load_data('events.json')
    events = [e for e in events if e['id'] != event_id]
    
    save_data('events.json', events)
    flash('Мероприятие отклонено', 'success')
    return redirect(url_for('moderator_panel'))

# Одобрение НКО (модератор)
@app.route('/moderator/approve-nko/<int:nko_id>', methods=['POST'])
@role_required(['moderator', 'admin'])
def approve_nko(nko_id):
    nko_data = load_data('nko.json')
    
    for nko in nko_data:
        if nko['id'] == nko_id:
            nko['approved'] = True
            nko['approved_at'] = datetime.now().isoformat()
            break
    
    save_data('nko.json', nko_data)
    flash('НКО одобрена', 'success')
    return redirect(url_for('moderator_panel'))

# Панель администратора
@app.route('/admin')
@role_required(['admin', 'moderator'])
def admin_panel():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    return render_template('admin_panel.html', 
                         translations=translations, 
                         lang=lang, 
                         user=user)

# Добавление новости (администратор)
@app.route('/admin/add-news', methods=['GET', 'POST'])
@role_required(['admin', 'moderator'])
def add_news():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    if request.method == 'POST':
        news_data = load_data('news.json')
        
        new_news = {
            'id': len(news_data) + 1,
            'title': request.form.get('title'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'city': request.form.get('city') if request.form.get('city') else None,
            'content': request.form.get('content'),
            'image': request.form.get('image'),
            'created_at': datetime.now().isoformat()
        }
        
        news_data.append(new_news)
        save_data('news.json', news_data)
        
        flash('Новость добавлена', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('add_news.html', translations=translations, lang=lang, user=user)

# Добавление материала в базу знаний (администратор)
@app.route('/admin/add-knowledge', methods=['GET', 'POST'])
@role_required(['admin', 'moderator'])
def add_knowledge():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    if request.method == 'POST':
        knowledge_data = load_data('knowledge.json')
        
        new_material = {
            'id': len(knowledge_data) + 1,
            'title': request.form.get('title'),
            'category': request.form.get('category'),
            'type': request.form.get('type'),
            'description': request.form.get('description'),
            'url': request.form.get('url'),
            'created_at': datetime.now().isoformat()
        }
        
        knowledge_data.append(new_material)
        save_data('knowledge.json', knowledge_data)
        
        flash('Материал добавлен в базу знаний', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('add_knowledge.html', translations=translations, lang=lang, user=user)

# Добавление НКО (пользователь)
@app.route('/profile/add-nko', methods=['GET', 'POST'])
@login_required
def add_nko():
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    if request.method == 'POST':
        nko_data = load_data('nko.json')
        
        new_nko = {
            'id': len(nko_data) + 1,
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'description': request.form.get('description'),
            'volunteers': request.form.get('volunteers'),
            'city': request.form.get('city'),
            'address': request.form.get('address'),
            'website': request.form.get('website'),
            'social': request.form.get('social'),
            'logo': request.form.get('logo'),
            'creator_id': user['id'],
            'approved': False,
            'created_at': datetime.now().isoformat()
        }
        
        nko_data.append(new_nko)
        save_data('nko.json', nko_data)
        
        flash('НКО создана и отправлена на модерацию', 'success')
        return redirect(url_for('profile'))
    
    return render_template('add_nko.html', translations=translations, lang=lang, user=user)

# API endpoints
@app.route('/api/cities/<lang>')
def get_cities(lang):
    cities = load_cities(lang)
    return jsonify(cities)

@app.route('/api/translations/<lang>')
def get_translations(lang):
    translations = load_translations(lang)
    return jsonify(translations)

@app.route('/api/set-city', methods=['POST'])
def set_city():
    data = request.get_json()
    session['city'] = data.get('city')
    return jsonify({'success': True})

@app.route('/api/set-lang', methods=['POST'])
def set_lang():
    data = request.get_json()
    session['lang'] = data.get('lang', 'ru')
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
