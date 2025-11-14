"""
Маршруты для авторизации и регистрации

Содержит:
- /login (GET, POST): вход в систему
- /register (GET, POST): регистрация нового пользователя
- /logout: выход из системы
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from utils import load_data, save_data, load_translations

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в систему"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
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
            return redirect(url_for('main.profile'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('login.html', translations=translations, lang=lang)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    
    # Передаем сегодняшнюю дату для ограничения выбора даты рождения
    from datetime import date
    today = date.today().isoformat()
    
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        birth_date = request.form.get('birthDate')
        email = request.form.get('email')
        password = request.form.get('password')
        city = request.form.get('city')
        
        users = load_data('users.json')
        
        if any(u['email'] == email for u in users):
            flash('Пользователь с таким email уже существует', 'error')
        else:
            # Формируем полное имя
            full_name = f"{first_name} {last_name}"
            
            new_user = {
                'id': len(users) + 1,
                'firstName': first_name,
                'lastName': last_name,
                'name': full_name,
                'birthDate': birth_date,
                'email': email,
                'password': password,
                'role': 'volunteer',
                'city': city,
                'created_at': datetime.now().isoformat()
            }
            users.append(new_user)
            save_data('users.json', users)
            
            flash('Регистрация успешна! Войдите в систему', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', translations=translations, lang=lang, today=today)


@auth_bp.route('/logout')
def logout():
    """Выход из системы"""
    session.pop('user', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('main.index'))
