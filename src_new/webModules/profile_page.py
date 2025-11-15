from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session



def before_profile_page(request):
    if 'username' in session:
        return profile_page(request=request, mail=session['username'])

    return redirect('/login')


def profile_page(request, mail):
    data_db = UsersDB_module().select_with_mail(mail=mail)
    data_db.pop('user_pass')
    return render_template('profile.html', data_profile=data_db)