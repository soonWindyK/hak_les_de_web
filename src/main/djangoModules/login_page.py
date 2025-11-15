from src.main.databaseModules.classUsersDB import UsersDB_module
from hash_password_usr import hasher_pass
from flask import redirect, url_for, render_template


def login_page(request):
    user_mail = request.form['email']
    password = hasher_pass(request.form['password'])
    print(user_mail, password)

    if UsersDB_module().check_presence_mail(mail=user_mail):
        user = UsersDB_module().select_with_mail(mail=user_mail)

        if user['user_pass'] == password:
            return redirect(url_for('lk'))
        else:
            return render_template('login.html', message='Пароль неверный')
    else:
        return render_template('login.html', message='Пользователь не найден')

