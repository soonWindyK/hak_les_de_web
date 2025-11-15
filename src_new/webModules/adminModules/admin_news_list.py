from flask import render_template, redirect, url_for, session
from databaseModules.classNewsDB import NewssDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from ..upload_file_from_flask import handle_file_upload
from databaseModules.classCityRegionDB import CityRegionDB_module


def before_admin_news():
    if 'username' in session:
        data_db = UsersDB_module().select_with_mail(mail=session['username'])
        if data_db['user_role'] == 2:
            return admin_news_()
        else:
            return redirect('/news')

    return redirect('/login')


def admin_news_():
    news = NewssDB_module().get_all_news()
    print(news)

    if request.method == 'POST':
        action = request.form.get('action', None)
        if "new_" in action:
            new_id = int(action.split("_")[-1])

            if NewssDB_module().delete_new(new_id):
                print('Удалено')
                news = NewssDB_module().get_all_news()
            else:
                flash('Ивент не удалось удалить','error')


    return render_template('admin/admin-news-list.html', news=news)
