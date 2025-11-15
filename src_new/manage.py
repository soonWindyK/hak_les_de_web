from flask import Flask, render_template, session, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/')
def home(): return render_template('index.html')

@app.route('/calendar')
def calendar(): return render_template('calendar.html')
@app.route('/knowledge')
def knowledge(): return render_template('knowledge.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from webModules.login_page import before_login_page
    return before_login_page(request=request.form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    from webModules.registration_page import before_reg_page
    return before_reg_page(request=request.form)

@app.route('/news')
def news(): return render_template('news.html')
@app.route('/news/<int:news_id>')
def news_detail(news_id): return render_template('news-detail.html')
@app.route('/nko')
def nko(): return render_template('nko.html')
@app.route('/nko/<int:nko_id>')
def nko_detail(nko_id): return render_template('nko-detail.html')

@app.route('/profile')
def profile():
    from webModules.profile_page import before_profile_page
    return before_profile_page(request=request.form)

@app.route('/logout')
def logout():
    # Здесь будет логика выхода из системы
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/panel')
def admin_panel():
    # Проверка роли пользователя
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return render_template('admin/admin-panel.html')
    elif user_role == 'moderator':
        return render_template('moderator/moderator-panel.html')
    else:
        return redirect(url_for('home'))

# Маршруты для администратора - НКО
@app.route('/admin/nko')
def admin_nko_list():
    # Здесь будет логика отображения списка НКО
    return render_template('admin/admin-nko-list.html')

@app.route('/admin/nko/add')
def admin_nko_add():
    # Здесь будет логика добавления НКО
    return render_template('admin/admin-nko-add.html')

# Маршруты для администратора - Новости
@app.route('/admin/news')
def admin_news_list():
    # Здесь будет логика отображения списка новостей
    return render_template('admin/admin-news-list.html')

@app.route('/admin/news/add')
def admin_news_add():
    # Здесь будет логика добавления новости
    return render_template('admin/admin-news-add.html')

# Маршруты для администратора - События
@app.route('/admin/events')
def admin_events_list():
    # Здесь будет логика отображения списка событий
    return render_template('admin/admin-events-list.html')

@app.route('/admin/events/add')
def admin_events_add():
    # Здесь будет логика добавления события
    return render_template('admin/admin-events-add.html')

# Маршруты для администратора - База знаний
@app.route('/admin/knowledge')
def admin_knowledge_list():
    # Здесь будет логика отображения списка материалов
    return render_template('admin/admin-knowledge-list.html')

@app.route('/admin/knowledge/add')
def admin_knowledge_add():
    # Здесь будет логика добавления материала
    return render_template('admin/admin-knowledge-add.html')

# Маршруты для модератора - НКО
@app.route('/moderator/nko/pending')
def moderator_nko_pending():
    # Здесь будет логика отображения НКО на модерации
    return render_template('moderator/moderator-nko-pending.html')

@app.route('/moderator/nko/all')
def moderator_nko_all():
    # Здесь будет логика отображения всех НКО
    return render_template('moderator/moderator-nko-all.html')

# Маршруты для модератора - События
@app.route('/moderator/events/pending')
def moderator_events_pending():
    # Здесь будет логика отображения событий на модерации
    return render_template('moderator/moderator-events-pending.html')

@app.route('/moderator/events/all')
def moderator_events_all():
    # Здесь будет логика отображения всех событий
    return render_template('moderator/moderator-events-all.html')

# Маршруты для модератора - Статистика
@app.route('/moderator/stats')
def moderator_stats():
    # Здесь будет логика отображения статистики
    return render_template('moderator/moderator-stats.html')

if __name__ == '__main__':
    app.run(debug=True)