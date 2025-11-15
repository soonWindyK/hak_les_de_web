from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from webModules.hash_password_usr import hasher_pass



def before_profile_page(request):
    if 'username' in session:
        print(request)
        return profile_page(request=request, mail=session['username'])

    return redirect('/login')


def profile_page(request, mail):
    data_db = UsersDB_module().select_with_mail(mail=mail)
    data_db.pop('user_pass')
    action = request.form.get('action')

    if action == 'btn-save-password':
        data_db = UsersDB_module().select_with_mail(mail=mail)
        print(data_db)

        old_pass = request.form.get('current_password')
        new_pass = request.form.get('new_password')
        confirm_pass = request.form.get('confirm_password')

        if hasher_pass(old_pass) != data_db['user_pass']:
            return render_template('profile.html', data_profile=data_db, error_pass='Неверный текущий пароль')

        if new_pass != confirm_pass:
            return render_template('profile.html', data_profile=data_db, error_pass='Новые пароли не совпадают')
        else:
            if UsersDB_module().update_password(mail=mail, password=hasher_pass(new_pass)):
                return render_template('profile.html', data_profile=data_db, succes_pass='Пароль обновлён')
            else:
                return render_template('profile.html', data_profile=data_db, error_pass='Ошибка при обновлении пароля')

    return render_template('profile.html', data_profile=data_db)