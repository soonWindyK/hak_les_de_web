from flask import session, redirect
from databaseModules.classUsersDB import UsersDB_module

def check_admin():
    if 'username' in session:
        data_db = UsersDB_module().select_with_mail(mail=session['username'])
        if data_db['user_role'] == 2:
            return True

    return redirect('/')