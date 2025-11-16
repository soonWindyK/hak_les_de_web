from databaseModules.classUsersDB import UsersDB_module
from webModules.hash_password_usr import hasher_pass
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

    if hasher_pass(old_pass) == data_db['user_pass']:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Неверный текущий пароль')

    if new_pass != confirm_pass:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Новые пароли не совпадают')

    if UsersDB_module().update_password(mail=mail, password=hasher_pass(new_pass)):
        return render_template('profile.html', data_profile=data_db_copy, succes_pass='Пароль успешно обновлён')
    else:
        return render_template('profile.html', data_profile=data_db_copy, error_pass='Ошибка при обновлении пароля')

def change_profile(request, mail):
    request = request.form
    data_db = UsersDB_module().select_with_mail(mail=mail)

    form_data = {
        'first_name': request.get('first_name', ''),
        'last_name': request.get('last_name', ''),
        'father_name': request.get('father_name', ''),
        'birth_date': request.get('birth_date', '')
    }

    data = list(form_data.values())

    form_data = data_db | form_data

    if UsersDB_module().update_user(data, mail):
        return render_template('profile.html', data_profile=form_data, success_msg='Обновлено')
    else:
        return render_template('profile.html', data_profile=form_data, error_msg='Ошибка')


def profile_page(request, mail):
    data_db = UsersDB_module().select_with_mail(mail=mail)
    data_db.pop('user_pass', None)

    action = None
    if request.method == 'POST':
        action = request.form.get('action')

    if action == 'btn-save-password':
        return change_password(request=request, mail=mail)

    if action == 'change-profile':
        return change_profile(request=request, mail=mail)

    return render_template('profile.html', data_profile=data_db)
