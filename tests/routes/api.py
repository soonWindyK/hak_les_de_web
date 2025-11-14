"""
API endpoints для AJAX запросов

Содержит:
- /api/cities/<lang>: получение списка городов
- /api/translations/<lang>: получение переводов
- /api/set-city: установка выбранного города
- /api/set-lang: установка языка
"""

from flask import Blueprint, jsonify, request, session
from utils import load_cities, load_translations

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/cities/<lang>')
def get_cities(lang):
    """Получение списка городов для указанного языка"""
    cities = load_cities(lang)
    return jsonify(cities)


@api_bp.route('/api/translations/<lang>')
def get_translations(lang):
    """Получение переводов для указанного языка"""
    translations = load_translations(lang)
    return jsonify(translations)


@api_bp.route('/api/set-city', methods=['POST'])
def set_city():
    """Установка выбранного города в сессию"""
    data = request.get_json()
    session['city'] = data.get('city')
    return jsonify({'success': True})


@api_bp.route('/api/set-lang', methods=['POST'])
def set_lang():
    """Установка языка в сессию"""
    data = request.get_json()
    session['lang'] = data.get('lang', 'ru')
    return jsonify({'success': True})
