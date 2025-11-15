from databaseModules.classUsersDB import UsersDB_module
from webModules.hash_password_usr import verify_password
from flask import redirect, render_template, session


def before_login_page(request):
    if 'username' not in session:
        if request.method == 'POST':
            return login_page(request=request.form)

        return render_template('login.html')
    else:
        return redirect('/profile')


def login_page(request):
    user_mail = request.get('email', '').strip()
    password = request.get('password', '')

    if not user_mail or not password:
        return render_template('login.html', error_msg='Заполните все поля')

    if UsersDB_module().check_presence_mail(mail=user_mail):
        user = UsersDB_module().select_with_mail(mail=user_mail)

        if verify_password(password, user['user_pass']):
            session['username'] = user_mail
            session['user_role'] = user['user_role']
            session['user_id'] = user['user_id']
            return redirect('/profile')
        else:
            return render_template('login.html', error_msg='Неверный пароль')
    else:
        return render_template('login.html', error_msg='Пользователь не найден')

