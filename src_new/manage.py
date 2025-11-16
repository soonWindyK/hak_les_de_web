from flask import Flask, render_template, session, redirect, url_for, request
from databaseModules.classUsersDB import UsersDB_module
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
app = Flask(__name__, static_folder='static',static_url_path='/static')
app.secret_key = 'your-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#Рендеринг главной страницы
@app.route('/', methods=['GET', 'POST'])
def home(): return render_template('index.html')

#Рендеринг страницы календаря
@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    from webModules.eventsModules.calendar import before_calendar
    return before_calendar()

#Рендеринг страницы курсов
@app.route('/knowledge', methods=['GET', 'POST'])
def knowledge():
    from webModules.knowelegeModules.courses_page import before_courses
    return before_courses(request=request)
#Рендеринг рендер страницы тем в курсах
@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
    from webModules.knowelegeModules.courses_page import course_detail_page
    return course_detail_page(course_id)
#Рендеринг карты НКО
@app.route('/nko/map')
def nko_map(): return render_template('nko-map.html')
#Рендеринг темы
@app.route('/theme/<int:theme_id>', methods=['GET', 'POST'])
def theme_detail(theme_id):
    from webModules.knowelegeModules.courses_page import theme_detail_page
    return theme_detail_page(theme_id)
#Рендеринг страницы авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    from webModules.login_page import before_login_page
    return before_login_page(request=request)
#Рендеринг страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    from webModules.registration_page import before_reg_page
    return before_reg_page(request=request)
#Рендеринг страницы новостей
@app.route('/news', methods=['GET', 'POST'])
def news():
    from webModules.newsModules.news import before_news
    return before_news()
#Рендеринг страницы подробнее по новости
@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news_detail(news_id):
    return render_template('news-detail.html')
#Рендеринг страницы списка НКО
@app.route('/nko', methods=['GET', 'POST'])
def nko():
    from webModules.nkoModules.nko import nko_
    return nko_(request=request)

# @app.route('/nko/<int:nko_id>', methods=['GET', 'POST'])
# def nko_detail(nko_id):
#     return render_template('nko-detail.html')
#Рендеринг стираницы профиля
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    from webModules.profile_page import before_profile_page
    return before_profile_page(request=request)
#системы выхода из аккаунта
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


#Рендеринг панели администратора в профиле
@app.route('/admin/panel', methods=['GET', 'POST'])
def admin_panel():
    from webModules.adminModules.admin_panel import admin_panel

    if 'username' in session:
        mail = session['username']
        data_db = UsersDB_module().select_with_mail(mail=mail)
        user_role = data_db['role_id']
        print(session)

        if user_role == 2:  # admin
            return admin_panel(request)
        elif user_role == 3:  # moder
            data_db.pop('user_pass', None)
            return render_template('moderator/moderator-panel.html', data_profile=data_db)

    return redirect('/')


# Ренедеринг страницы нко в админ панели
@app.route('/admin/nko', methods=['GET', 'POST'])
def admin_nko_list():
    # Здесь будет логика отображения списка НКО
    from webModules.adminModules.admin_nko_list import before_admin_nko_
    return before_admin_nko_()


@app.route('/profile/favorites')
def favorites():
    data_profile = UsersDB_module().select_with_mail(mail=session['username'])
    return render_template('favorites.html', data_profile=data_profile)

#рендеринг страницы добавления НКО
@app.route('/nko/add', methods=['GET', 'POST'])
def nko_add():
    from webModules.nkoModules.nko_add import before_nko_add
    # Здесь будет логика добавления НКО
    return before_nko_add(request=request)


# Рендеринг страницы новостей в админ панели
@app.route('/admin/news', methods=['GET', 'POST'])
def admin_news_list():
    from webModules.adminModules.admin_news_list import before_admin_news
    return before_admin_news()
# Рендеринг страницы добавления новости у админа
@app.route('/admin/news/add', methods=['GET', 'POST'])
@csrf.exempt
def admin_news_add():
    from webModules.newsModules.admin_news_add import before_admin_new_add
    return before_admin_new_add()


# Рендеринг страницы событий в админ панели
@app.route('/admin/events', methods=['GET', 'POST'])
def admin_events_list():
    from webModules.adminModules.admin_events_list import before_admin_events
    return before_admin_events()
#рендеринг страницы добавления события
@app.route('/event/add', methods=['GET', 'POST'])
def admin_events_add():
    from webModules.eventsModules.admin_event_add import before_admin_event_add
    # Здесь будет логика добавления события
    return before_admin_event_add()

# Рендеринг страницы для администратора - База знаний (Курсы)
@app.route('/admin/courses', methods=['GET', 'POST'])
def admin_courses_list():
    from webModules.adminModules.admin_courses_list import admin_courses_list
    return admin_courses_list()
#рендеринг страницы добавления курса в админ панели
@app.route('/admin/course/add', methods=['GET', 'POST'])
def admin_course_add():
    from webModules.adminModules.admin_courses_list import admin_course_add
    return admin_course_add(request)
#Рендеринг страницы курса
@app.route('/admin/course/<int:course_id>', methods=['GET', 'POST'])
def admin_course_detail(course_id):
    from webModules.adminModules.admin_courses_list import admin_course_detail
    return admin_course_detail(course_id)
#рендеринг страницы редактирования курса в админ панели
@app.route('/admin/course/edit/<int:course_id>', methods=['GET', 'POST'])
def admin_course_edit(course_id):
    from webModules.adminModules.admin_course_edit import before_admin_course_edit
    return before_admin_course_edit(course_id)
#рендеринг страницы добавления темы в админ панели
@app.route('/admin/course/<int:course_id>/theme/add', methods=['GET', 'POST'])
def admin_theme_add(course_id):
    from webModules.adminModules.admin_courses_list import admin_theme_add
    return admin_theme_add(course_id)
#редеринг страницы редактирования темы в админ панели
@app.route('/admin/theme/<int:theme_id>/edit', methods=['GET', 'POST'])
def admin_theme_edit(theme_id):
    from webModules.adminModules.admin_courses_list import admin_theme_edit
    return admin_theme_edit(request, theme_id)
#удаление темы в админ панели
@app.route('/admin/theme/<int:theme_id>/delete', methods=['POST'])
def admin_theme_delete(theme_id):
    from webModules.adminModules.admin_courses_list import admin_theme_delete
    return admin_theme_delete(request, theme_id)

# Маршруты для модератора - НКО
@app.route('/moderator/nko/pending', methods=['GET', 'POST'])
def moderator_nko_pending():
    from webModules.moderatorModules.moderatr_nko_pending import before_moder_nko_pending
    return before_moder_nko_pending()

@app.route('/moderator/nko/all', methods=['GET', 'POST'])
def moderator_nko_all():
    # Здесь будет логика отображения всех НКО
    return render_template('moderator/moderator-nko-all.html')

# Маршруты для модератора - События
@app.route('/moderator/events/pending', methods=['GET', 'POST'])
def moderator_events_pending():
    # Здесь будет логика отображения событий на модерации
    from webModules.moderatorModules.moderatr_events_pending import before_moder_events_pending
    return before_moder_events_pending()

@app.route('/moderator/events/all', methods=['GET', 'POST'])
def moderator_events_all():
    # Здесь будет логика отображения всех событий
    return render_template('moderator/moderator-events-all.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)