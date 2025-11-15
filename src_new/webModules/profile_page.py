from databaseModules.classUsersDB import UsersDB_module
from webModules.hash_password_usr import hasher_pass, verify_password
from flask import render_template, redirect, session


def before_profile_page(request):
    if 'username' in session:
        return profile_page(request=request, mail=session['username'])

    return redirect('/login')


def change_password(request, mail):
    data_db = UsersDB_module().select_with_mail(mail=mail)
    data_db_copy = data_db.copy()
    data_db_copy.pop('user_pass', None)

    old_pass = request.form.get('current_password', '')
    new_pass = request.form.get('new_password', '')
    confirm_pass = request.form.get('confirm_password', '')

    if not old_pass or not new_pass or not confirm_pass:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Заполните все поля')

    if not verify_password(old_pass, data_db['user_pass']):
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Неверный текущий пароль')

    if new_pass != confirm_pass:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Новые пароли не совпадают')
    
    if len(new_pass) < 6:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Пароль должен быть не менее 6 символов')

    if UsersDB_module().update_password(mail=mail, password=hasher_pass(new_pass)):
        return render_template('profile.html', data_profile=data_db_copy, succes_pass='Пароль успешно обновлён')
    else:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Ошибка при обновлении пароля')


def profile_page(request, mail):
    data_db = UsersDB_module().select_with_mail(mail=mail)
    data_db.pop('user_pass', None)

    action = None
    if request.method == 'POST':
        action = request.form.get('action')

    if action == 'btn-save-password':
        return change_password(request=request, mail=mail)

    return render_template('profile.html', data_profile=data_db)
