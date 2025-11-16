from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def before_nko_(request):
    return nko_(request=request)



def nko_(request):
    print(request)
    cities_list = CityRegionDB_module().get_cities_list_with_region()
    nko_list = False
    city_selected = region_sel = ''
    if request.method == 'POST':
        action = request.form.get('action')
        print(action, request.form)
        if action == 'filter_go':
            city_id = int(request.form.get('city').split("_")[-1])

            if city_id != 0:
                nko_list = NkoDB_module().get_nko_by_city_id(city_id=city_id)
                city_selected = f"{cities_list[city_id-1][1]}"
                region_sel = f"{cities_list[city_id-1][2]}"

        if 'favorite_add' in action:
            from src_new.databaseModules.classFavoriteUsersDB import FavoriteUsersDB_module
            if 'username' in session:
                type_post = 'nko'
                post_id = int(action.split("_")[-1])
                user_id = UsersDB_module().select_with_mail(mail=session['username'])['user_id']

                view_status = FavoriteUsersDB_module().presence_in_favorite(user_id, post_id, type_post)
                if view_status == 'error':
                    print('Не было в избарнном', view_status)
                else:
                    view_status = view_status['view_status']
                    update_status = FavoriteUsersDB_module().update_favorite(user_id, post_id, type_post, view_status)
                    print('Есть в избрном', update_status)

                # print(post_id, type_post, user_id)


    if nko_list == False:
        user_id = UsersDB_module().select_with_mail(mail=session['username'])['user_id']
        nko_list = NkoDB_module().get_all_nko(user_id=user_id)

    cats_list = SmallFuncsDB_module().select_all_categories()


    return render_template('nko.html', nko_list=nko_list, cats_list=cats_list, cities_list=cities_list,
                           city_selected=city_selected, region_sel=region_sel)
