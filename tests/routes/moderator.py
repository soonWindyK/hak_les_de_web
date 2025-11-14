"""
Маршруты для панели модератора

Содержит:
- /moderator: панель модератора
- /moderator/approve-event/<id>: одобрение мероприятия
- /moderator/reject-event/<id>: отклонение мероприятия
- /moderator/approve-nko/<id>: одобрение НКО
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash
from datetime import datetime
from decorators import role_required
from utils import load_data, save_data, load_translations

moderator_bp = Blueprint('moderator', __name__)


@moderator_bp.route('/moderator')
@role_required(['moderator', 'admin'])
def moderator_panel():
    """Панель модератора"""
    lang = session.get('lang', 'ru')
    translations = load_translations(lang)
    user = session.get('user')
    
    pending_events = [e for e in load_data('events.json') if not e.get('approved', False)]
    pending_nko = [n for n in load_data('nko.json') if not n.get('approved', False)]
    
    return render_template('moderator_panel.html', 
                         translations=translations, 
                         lang=lang, 
                         user=user,
                         pending_events=pending_events,
                         pending_nko=pending_nko)


@moderator_bp.route('/moderator/approve-event/<int:event_id>', methods=['POST'])
@role_required(['moderator', 'admin'])
def approve_event(event_id):
    """Одобрение мероприятия"""
    events = load_data('events.json')
    
    for event in events:
        if event['id'] == event_id:
            event['approved'] = True
            event['approved_at'] = datetime.now().isoformat()
            break
    
    save_data('events.json', events)
    flash('Мероприятие одобрено', 'success')
    return redirect(url_for('moderator.moderator_panel'))


@moderator_bp.route('/moderator/reject-event/<int:event_id>', methods=['POST'])
@role_required(['moderator', 'admin'])
def reject_event(event_id):
    """Отклонение мероприятия"""
    events = load_data('events.json')
    events = [e for e in events if e['id'] != event_id]
    
    save_data('events.json', events)
    flash('Мероприятие отклонено', 'success')
    return redirect(url_for('moderator.moderator_panel'))


@moderator_bp.route('/moderator/approve-nko/<int:nko_id>', methods=['POST'])
@role_required(['moderator', 'admin'])
def approve_nko(nko_id):
    """Одобрение НКО"""
    nko_data = load_data('nko.json')
    
    for nko in nko_data:
        if nko['id'] == nko_id:
            nko['approved'] = True
            nko['approved_at'] = datetime.now().isoformat()
            break
    
    save_data('nko.json', nko_data)
    flash('НКО одобрена', 'success')
    return redirect(url_for('moderator.moderator_panel'))
