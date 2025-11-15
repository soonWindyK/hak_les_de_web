from ..databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect
from ..djangoModules.hash_password_usr import hasher_pass
import datetime


def reg_page(request):
    first_name = request['first_name']
    last_name = request['last_name']
    father_name = request.get('patronymic', '')
    user_mail = request['email']
    password = request['password']
    hash_password = hasher_pass(password=password)
    user_birthday = request.get('birthday',datetime.datetime.now())
    user_role = 1
    city_id = 1

    # нужно сделать приход с бд
    if UsersDB_module().check_presence_mail(mail=user_mail):
        return render_template('register.html')
    else:
        UsersDB_module().new_user(data=(
            first_name,
            last_name,
            father_name,
            user_role,
            user_birthday,
            user_mail,
            hash_password,
            city_id,)
        )
        return redirect('login')