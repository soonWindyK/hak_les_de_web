from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from webModules.hash_password_usr import hasher_pass


def before_admin_panel(request):
    pass



def admin_panel(request):
    mail = session['username']
    data_db = UsersDB_module().select_with_mail(mail=mail)
    data_db.pop('user_pass', None)
    
    return render_template('admin/admin-panel.html', data_profile=data_db)