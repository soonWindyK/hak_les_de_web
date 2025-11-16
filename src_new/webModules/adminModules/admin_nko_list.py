from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def before_admin_nko_():
    if 'username' in session:
        data_db = UsersDB_module().select_with_mail(mail=session['username'])
        if data_db['user_role'] == 2:
            return admin_nko_()

    return redirect('/')


def admin_nko_():
    cats_list = SmallFuncsDB_module().select_all_categories()

    if request.method == 'POST':
        action = request.form.get('action', None)

        if "nko_" in action:
            nko_id = int(action.split("_")[-1])

            if NkoDB_module().delete_nko(nko_id):
                print('Удалено')
            else:
                flash('Ивент не удалось','error')

    user_id = UsersDB_module().select_with_mail(mail=session['username'])['user_id']
    nko_list = NkoDB_module().get_all_nko(user_id=user_id)
    return render_template('admin/admin-nko-list.html', nko_list=nko_list, cats_list=cats_list)
