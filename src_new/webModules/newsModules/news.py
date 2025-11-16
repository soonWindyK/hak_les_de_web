from flask import render_template, redirect, url_for, session
from databaseModules.classNewsDB import NewssDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from ..upload_file_from_flask import handle_file_upload
from databaseModules.classCityRegionDB import CityRegionDB_module


def before_news():
    return news_()



def news_():
    print(request)
    cities_list = CityRegionDB_module().get_cities_list_with_region()
    news = False

    city_selected = region_sel = ''
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'filter_go':
            city_id = int(request.form.get('city').split("_")[-1])

            if city_id != 0:
                news = NewssDB_module().get_new_by_city_id(city_id=city_id)
                city_selected = f"{cities_list[city_id-1][1]}"
                region_sel = f"{cities_list[city_id-1][2]}"


    if news == False:
        news = NewssDB_module().get_all_news()


    return render_template('news.html', news=news, cities_list=cities_list,
                           city_selected=city_selected, region_sel=region_sel)

# def news_():
#     return render_template('news.html', news=news)
