"""
Декораторы для проверки авторизации и ролей пользователей

Содержит:
- login_required: проверка авторизации пользователя
- role_required: проверка роли пользователя
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Декоратор для проверки авторизации.
    Перенаправляет на страницу входа, если пользователь не авторизован.
    
    Использование:
        @login_required
        def profile():
            return "Личный кабинет"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(roles):
    """
    Декоратор для проверки роли пользователя.
    Перенаправляет на главную, если у пользователя нет нужной роли.
    
    Параметры:
        roles (list): список разрешенных ролей
    
    Использование:
        @role_required(['admin', 'moderator'])
        def admin_panel():
            return "Панель администратора"
    """
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
