from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

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

@app.route('/')
def index():
    lang = request.args.get('lang', 'ru')
    translations = load_translations(lang)
    return render_template('index.html', translations=translations, lang=lang)

@app.route('/api/cities/<lang>')
def get_cities(lang):
    cities = load_cities(lang)
    return jsonify(cities)

@app.route('/api/translations/<lang>')
def get_translations(lang):
    translations = load_translations(lang)
    return jsonify(translations)

if __name__ == '__main__':
    app.run(debug=True)
