from src.databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, url_for
from hash_password import hash_pass

def reg_page(request):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    father_name = request.form['father_name']
    user_mail = request.form['email']
    password = request.form['password']
    hash_password = hash_pass(password=password)
    user_birthday = request.form['birthday']
    user_role = 1

    # нужно сделать приход с бд


    if UsersDB_module().check_presence_mail(mail=user_mail):
        return render_template('register.html', message2='Почта занята')
    else:
        UsersDB_module().new_user(
    first_name,
            last_name,
            father_name,
            user_role,
            user_birthday,
            user_mail,
            hash_password
        )
        return redirect(url_for('login'))