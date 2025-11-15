from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect
from webModules.hash_password_usr import hasher_pass
import datetime


def before_reg_page(request):
    if request.method == 'POST':
        return reg_page(request=request.form)

    return render_template('register.html')

def reg_page(request):
    form_data = {
        'first_name': request.get('first_name', ''),
        'last_name': request.get('last_name', ''),
        'father_name': request.get('father_name', ''),
        'email': request.get('email', ''),
        'city_id': request.get('city_id', ''),
        'birthday': request.get('birth_date', '')
    }

    first_name = request['first_name']
    last_name = request['last_name']
    father_name = request.get('father_name', '')
    user_mail = request['email']
    password = request['password']
    password_confirm = request['password_confirm']
    hash_password = hasher_pass(password=password)
    user_birthday = request.get('birth_date', datetime.datetime.now())
    user_role = 1
    city_id = 1

    if password != password_confirm:
        return render_template('register.html', error_pass='Пароли разные!', form_data=form_data)

    # нужно сделать приход с бд
    if UsersDB_module().check_presence_mail(mail=user_mail):
        return render_template('register.html', error_mail='Почта используется!', form_data=form_data)
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