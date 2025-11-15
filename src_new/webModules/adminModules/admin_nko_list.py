from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def before_admin_nko_():
    return admin_nko_()


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

    nko_list = NkoDB_module().get_all_nko()
    return render_template('admin/admin-nko-list.html', nko_list=nko_list, cats_list=cats_list)
