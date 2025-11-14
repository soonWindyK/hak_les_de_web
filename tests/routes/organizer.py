"""
Маршруты для панели организатора

Содержит:
- /organizer: панель организатора
- /organizer/create-event: создание мероприятия
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from decorators import role_required, login_required
from utils import load_data, save_data, load_translations

organizer_bp = Blueprint('organizer', __name__)


@organizer_bp.route('/organizer')
@role_required(['organizer', 'moderator', 'admin'])
def organizer_panel():
    """Панель организатора"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    events = load_data('events.json')
    my_events = [e for e in events if e.get('organizer_id') == user['id']]
    
    return render_template('organizer_panel.html', 
                         translations=translations, 
                         lang=lang, 
                         user=user,
                         my_events=my_events)


@organizer_bp.route('/organizer/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    """Создание мероприятия - доступно всем зарегистрированным пользователям"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    if request.method == 'POST':
        events = load_data('events.json')
        
        # Модераторы и администраторы могут создавать события без модерации
        auto_approve = user['role'] in ['moderator', 'admin']
        
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
            'approved': auto_approve,
            'created_at': datetime.now().isoformat()
        }
        
        events.append(new_event)
        save_data('events.json', events)
        
        if auto_approve:
            flash('Мероприятие создано и опубликовано', 'success')
        else:
            flash('Мероприятие создано и отправлено на модерацию', 'success')
        
        return redirect(url_for('main.calendar'))
    
    return render_template('create_event.html', translations=translations, lang=lang, user=user)
