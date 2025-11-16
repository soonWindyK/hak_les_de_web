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
        action = request.form.get('action')
        if action == 'filter_go':
            city_id = int(request.form.get('city').split("_")[-1])
            nko_list = NkoDB_module().get_nko_by_city_id(city_id=city_id)
            print(action, city_id)

    else:
        nko_list = NkoDB_module().get_all_nko()


    cats_list = SmallFuncsDB_module().select_all_categories()
    cities_list = CityRegionDB_module().get_cities_list_with_region()


    return render_template('nko.html', nko_list=nko_list, cats_list=cats_list, cities_list=cities_list)
