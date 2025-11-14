"""
Маршруты для работы с НКО

Содержит:
- /profile/add-nko: создание НКО пользователем
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from decorators import login_required
from utils import load_data, save_data, load_translations

nko_bp = Blueprint('nko', __name__)


@nko_bp.route('/profile/add-nko', methods=['GET', 'POST'])
@login_required
def add_nko():
    """Создание НКО пользователем"""
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
        return redirect(url_for('main.profile'))
    
    return render_template('add_nko.html', translations=translations, lang=lang, user=user)
