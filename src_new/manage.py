from flask import Flask, render_template, session, redirect, url_for, request
from datetime import datetime
from databaseModules.classUsersDB import UsersDB_module

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def home(): return render_template('index.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar(): return render_template('calendar.html')
@app.route('/knowledge', methods=['GET', 'POST'])
def knowledge():
    from webModules.coursesModules.courses_page import courses_list_page
    return courses_list_page()

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
    from webModules.coursesModules.courses_page import course_detail_page
    return course_detail_page(course_id)

@app.route('/nko/map')
def nko_map():
    return render_template('nko-map.html')

@app.route('/theme/<int:theme_id>', methods=['GET', 'POST'])
def theme_detail(theme_id):
    from webModules.coursesModules.courses_page import theme_detail_page
    return theme_detail_page(theme_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from webModules.login_page import before_login_page
    return before_login_page(request=request)

@app.route('/register', methods=['GET', 'POST'])
def register():
    from webModules.registration_page import before_reg_page
    return before_reg_page(request=request)

@app.route('/news', methods=['GET', 'POST'])
def news(): return render_template('news.html')
@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news_detail(news_id):
    return render_template('news-detail.html')

@app.route('/nko', methods=['GET', 'POST'])
def nko():
    from webModules.nkoModules.nko import nko_
    return nko_(request=request)

@app.route('/nko/<int:nko_id>', methods=['GET', 'POST'])
def nko_detail(nko_id):
    return render_template('nko-detail.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    from webModules.profile_page import before_profile_page
    return before_profile_page(request=request)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Здесь будет логика выхода из системы
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/panel', methods=['GET', 'POST'])
def admin_panel():
    from webModules.adminModules.admin_panel import admin_panel

    user_role = UsersDB_module().select_with_mail(mail=session['username'])['role_id']
    print(session)

    if user_role == 2:  # admin
        return admin_panel(request)
    elif user_role == 3:  # moder
        return render_template('moderator/moderator-panel.html')
    else:
        return redirect('/')


# Маршруты для администратора - НКО
@app.route('/admin/nko', methods=['GET', 'POST'])
def admin_nko_list():
    # Здесь будет логика отображения списка НКО
    return render_template('admin/admin-nko-list.html')

@app.route('/nko/add', methods=['GET', 'POST'])
def nko_add():
    from webModules.nkoModules.nko_add import before_nko_add
    # Здесь будет логика добавления НКО
    return before_nko_add(request=request)


# Маршруты для администратора - Новости
@app.route('/admin/news', methods=['GET', 'POST'])
def admin_news_list():
    # Здесь будет логика отображения списка новостей
    return render_template('admin/admin-news-list.html')

@app.route('/admin/news/add', methods=['GET', 'POST'])
def admin_news_add():
    # Здесь будет логика добавления новости
    return render_template('admin/admin-news-add.html')

# Маршруты для администратора - События
@app.route('/admin/events', methods=['GET', 'POST'])
def admin_events_list():
    # Здесь будет логика отображения списка событий
    return render_template('admin/admin-events-list.html')

@app.route('/admin/events/add', methods=['GET', 'POST'])
def admin_events_add():
    # Здесь будет логика добавления события
    return render_template('admin/admin-events-add.html')

# Маршруты для администратора - База знаний (Курсы)
@app.route('/admin/courses', methods=['GET', 'POST'])
def admin_courses_list():
    from webModules.adminModules.admin_courses import admin_courses_list
    return admin_courses_list(request)

@app.route('/admin/course/add', methods=['GET', 'POST'])
def admin_course_add():
    from webModules.adminModules.admin_courses import admin_course_add
    return admin_course_add(request)

@app.route('/admin/course/<int:course_id>', methods=['GET', 'POST'])
def admin_course_detail(course_id):
    from webModules.adminModules.admin_courses import admin_course_detail
    return admin_course_detail(request, course_id)

@app.route('/admin/course/<int:course_id>/theme/add', methods=['GET', 'POST'])
def admin_theme_add(course_id):
    from webModules.adminModules.admin_courses import admin_theme_add
    return admin_theme_add(request, course_id)

@app.route('/admin/theme/<int:theme_id>/edit', methods=['GET', 'POST'])
def admin_theme_edit(theme_id):
    from webModules.adminModules.admin_courses import admin_theme_edit
    return admin_theme_edit(request, theme_id)

@app.route('/admin/theme/<int:theme_id>/delete', methods=['POST'])
def admin_theme_delete(theme_id):
    from webModules.adminModules.admin_courses import admin_theme_delete
    return admin_theme_delete(request, theme_id)

# Маршруты для модератора - НКО
@app.route('/moderator/nko/pending', methods=['GET', 'POST'])
def moderator_nko_pending():
    # Здесь будет логика отображения НКО на модерации
    return render_template('moderator/moderator-nko-pending.html')

@app.route('/moderator/nko/all', methods=['GET', 'POST'])
def moderator_nko_all():
    # Здесь будет логика отображения всех НКО
    return render_template('moderator/moderator-nko-all.html')

# Маршруты для модератора - События
@app.route('/moderator/events/pending', methods=['GET', 'POST'])
def moderator_events_pending():
    # Здесь будет логика отображения событий на модерации
    return render_template('moderator/moderator-events-pending.html')

@app.route('/moderator/events/all', methods=['GET', 'POST'])
def moderator_events_all():
    # Здесь будет логика отображения всех событий
    return render_template('moderator/moderator-events-all.html')

# Маршруты для модератора - Статистика
@app.route('/moderator/stats', methods=['GET', 'POST'])
def moderator_stats():
    # Здесь будет логика отображения статистики
    return render_template('moderator/moderator-stats.html')

if __name__ == '__main__':
    app.run(debug=True)