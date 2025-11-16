from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def before_nko_(request):
    return nko_(request=request)

def filter(city_id):
    if city_id == 0:
        return NkoDB_module().get_all_nko()

    nko_list = NkoDB_module().get_nko_by_city_id(city_id=city_id)
    return nko_list


def nko_(request):
    print(request)
    cities_list = CityRegionDB_module().get_cities_list_with_region()
    nko_list = False
    city_selected = region_sel = ''
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'filter_go':
            city_id = int(request.form.get('city').split("_")[-1])

            if city_id != 0:
                nko_list = NkoDB_module().get_nko_by_city_id(city_id=city_id)
                city_selected = f"{cities_list[city_id-1][1]}"
                region_sel = f"{cities_list[city_id-1][2]}"


    if nko_list == False:
        nko_list = NkoDB_module().get_all_nko()

    cats_list = SmallFuncsDB_module().select_all_categories()


    return render_template('nko.html', nko_list=nko_list, cats_list=cats_list, cities_list=cities_list,
                           city_selected=city_selected, region_sel=region_sel)
