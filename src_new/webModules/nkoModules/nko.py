from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def before_nko_(request):
    return nko_(request=request)


def nko_(request):
    print(request)
    if request.method == 'POST':
        action = request.form.get('action', None)
        print(action)

    nko_list = NkoDB_module().get_all_nko()
    cats_list = SmallFuncsDB_module().select_all_categories()

    return render_template('nko.html', nko_list=nko_list, cats_list=cats_list)
