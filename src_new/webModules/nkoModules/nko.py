from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def before_nko_(request):
    return nko_(request=request)

def connect_nko_with_favor(nko_list, data_fav):
    for _, nko in enumerate(nko_list):
        nko_id = nko['nko_id']
        if not data_fav:
            continue

        if 'fav_id' in data_fav[0].keys():
            for favorit in data_fav:
                if favorit['post_id'] == nko_id:
                    nko_list[_]['view_status'] = favorit['view_status']
                    # print(nko_list[_])
                    continue

    return nko_list


from src_new.databaseModules.classFavoriteUsersDB import FavoriteUsersDB_module
def nko_(request):
    # print(request)
    cities_list = CityRegionDB_module().get_cities_list_with_region()

    msg_data = ''
    type_post = 'nko'

    nko_list = NkoDB_module().get_all_nko()

    if 'username' in session:
        user_id = UsersDB_module().select_with_mail(mail=session['username'])['user_id']

    if request.method == 'POST':
        action = request.form.get('action')
        # print(action, request.form)
        if action == 'filter_go':
            city_id = int(request.form.get('city').split("_")[-1])

            if city_id != 0:
                nko_list = NkoDB_module().get_nko_by_city_id(city_id=city_id)
                city_selected = f"{cities_list[city_id-1][1]}"
                region_sel = f"{cities_list[city_id-1][2]}"

        if 'favorite_add' in action:
            if 'username' in session:
                post_id = int(action.split("_")[-1])

                view_status = FavoriteUsersDB_module().presence_in_favorite(user_id, post_id, type_post)

                if view_status == 'error':
                    print('Не было в избарнном', view_status)
                    if FavoriteUsersDB_module().add_favorite(user_id, post_id, type_post):
                        pass
                    else:
                        msg_data = 'Ошибка добавления нового лайка'
                else:
                    view_status = view_status['view_status']
                    update_status = FavoriteUsersDB_module().update_favorite(user_id, post_id, type_post, view_status)

                    print('Есть в избранном', update_status)

                data_fav = FavoriteUsersDB_module().get_all_favorites_by_type_post(user_id, type_post)
                nko_list = connect_nko_with_favor(nko_list=nko_list, data_fav=data_fav)


    if 'username' in session:
        data_fav = FavoriteUsersDB_module().get_all_favorites_by_type_post(user_id, type_post)
        nko_list = connect_nko_with_favor(nko_list=nko_list, data_fav=data_fav)


    cats_list = SmallFuncsDB_module().select_all_categories()

    # print(nko_list)
    return render_template('nko.html', nko_list=nko_list, cats_list=cats_list, cities_list=cities_list,
                           msg_data=msg_data)
