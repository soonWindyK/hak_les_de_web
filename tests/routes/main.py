"""
Маршруты для главной страницы и публичных разделов

Содержит:
- /: главная страница
- /nko: список НКО
- /nko/<id>: страница НКО
- /knowledge: база знаний
- /calendar: календарь событий
- /news: новости
- /profile: личный кабинет
"""

from flask import Blueprint, render_template, request, session, redirect, url_for
from decorators import login_required
from utils import load_data, load_translations

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Главная страница"""
    lang = session.get('lang', 'ru')
    city = session.get('city', None)
    translations = load_translations(lang)
    return render_template('index.html', translations=translations, lang=lang, city=city)


@main_bp.route('/nko')
def nko_list():
    """Список НКО"""
    lang = session.get('lang', 'ru')
    city = request.args.get('city', session.get('city'))
    translations = load_translations(lang)
    nko_data = load_data('nko.json')
    
    if city:
        nko_data = [nko for nko in nko_data if nko.get('approved') and (nko.get('city') == city or not nko.get('city'))]
    else:
        nko_data = [nko for nko in nko_data if nko.get('approved')]
    
    return render_template('nko_list.html', translations=translations, lang=lang, nko_list=nko_data, city=city)


@main_bp.route('/nko/<int:nko_id>')
def nko_detail(nko_id):
    """Страница НКО"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    nko_data = load_data('nko.json')
    
    nko = next((n for n in nko_data if n['id'] == nko_id), None)
    if not nko:
        return "НКО не найдена", 404
    
    return render_template('nko_detail.html', translations=translations, lang=lang, nko=nko)


@main_bp.route('/knowledge')
def knowledge():
    """База знаний"""
    lang = session.get('lang', 'ru')
    category = request.args.get('category', 'all')
    translations = load_translations(lang)
    materials = load_data('knowledge.json')
    
    if category != 'all':
        materials = [m for m in materials if m.get('category') == category]
    
    return render_template('knowledge.html', translations=translations, lang=lang, materials=materials, category=category)


@main_bp.route('/calendar')
def calendar():
    """Календарь событий"""
    lang = session.get('lang', 'ru')
    city = request.args.get('city', session.get('city'))
    translations = load_translations(lang)
    events = load_data('events.json')
    
    events = [e for e in events if e.get('approved', False)]
    
    if city:
        events = [e for e in events if e.get('city') == city or not e.get('city')]
    
    return render_template('calendar.html', translations=translations, lang=lang, events=events, city=city)


@main_bp.route('/news')
def news():
    """Новости"""
    lang = session.get('lang', 'ru')
    city = request.args.get('city', session.get('city'))
    translations = load_translations(lang)
    news_data = load_data('news.json')
    
    if city:
        news_data = [n for n in news_data if n.get('city') == city or not n.get('city')]
    
    return render_template('news.html', translations=translations, lang=lang, news_list=news_data, city=city)


@main_bp.route('/profile')
@login_required
def profile():
    """Личный кабинет"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    favorites = session.get('favorites', {'news': [], 'events': [], 'materials': []})
    
    # Перенаправление на соответствующую панель в зависимости от роли
    if user['role'] == 'admin':
        return redirect(url_for('admin.admin_panel'))
    elif user['role'] == 'moderator':
        return redirect(url_for('moderator.moderator_panel'))
    elif user['role'] == 'organizer':
        return redirect(url_for('organizer.organizer_panel'))
    
    return render_template('profile.html', translations=translations, lang=lang, user=user, favorites=favorites)
