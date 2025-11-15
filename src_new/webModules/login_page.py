from databaseModules.classUsersDB import UsersDB_module
from webModules.hash_password_usr import hasher_pass
from flask import redirect, render_template, session


def before_login_page(request):
    if 'username' not in session:
        if request.method == 'POST':
            return login_page(request=request.form)

        return render_template('login.html')
    else:
        return redirect('/profile')


def login_page(request):
    user_mail = request['email']
    password = request['password']

    print(user_mail, password)

    if UsersDB_module().check_presence_mail(mail=user_mail):
        user = UsersDB_module().select_with_mail(mail=user_mail)

        if user['user_pass'] == hasher_pass(password):
            session['username'] = user_mail
            session['user_role'] = user['user_role']
            return redirect('/profile')
        else:
            return render_template('login.html', error_msg='Пароль неверный')
    else:
        return render_template('login.html', error_msg='Пользователь не найден')

