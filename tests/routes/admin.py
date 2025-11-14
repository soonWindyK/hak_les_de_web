"""
Маршруты для панели администратора

Содержит:
- /admin: панель администратора
- /admin/add-news: добавление новости
- /admin/add-knowledge: добавление материала в базу знаний
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from decorators import role_required
from utils import load_data, save_data, load_translations

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@role_required(['admin', 'moderator'])
def admin_panel():
    """Панель администратора"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    return render_template('admin_panel.html', translations=translations, lang=lang, user=user)


@admin_bp.route('/admin/add-news', methods=['GET', 'POST'])
@role_required(['admin', 'moderator'])
def add_news():
    """Добавление новости"""
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
        return redirect(url_for('admin.admin_panel'))
    
    return render_template('add_news.html', translations=translations, lang=lang, user=user)


@admin_bp.route('/admin/add-knowledge', methods=['GET', 'POST'])
@role_required(['admin', 'moderator'])
def add_knowledge():
    """Добавление материала в базу знаний"""
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
        return redirect(url_for('admin.admin_panel'))
    
    return render_template('add_knowledge.html', translations=translations, lang=lang, user=user)
