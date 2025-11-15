from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from webModules.hash_password_usr import hasher_pass



def before_admin_panel(request):
    pass



def admin_panel(request):
    return render_template('admin/admin-panel.html')