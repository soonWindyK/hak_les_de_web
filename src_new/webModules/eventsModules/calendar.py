from flask import render_template, redirect, url_for, session
from databaseModules.classEventsDB import EventsDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classFavoriteUsersDB import FavoriteUsersDB_module


def connect_events_with_favor(events, data_fav):
    for _, event in enumerate(events):
        event_id = event['id']
        if not data_fav:
            continue

        if 'fav_id' in data_fav[0].keys():
            for favorit in data_fav:
                if favorit['post_id'] == event_id:
                    events[_]['view_status'] = favorit['view_status']
                    # print(nko_list[_])
                    continue

    return events

def before_calendar():
    return calendar_()


def calendar_():
    cities_list = CityRegionDB_module().get_cities_list_with_region()
    print(request.form)

    msg_data = ''
    type_post = 'events'
    city_selected = region_sel = ''

    events = EventsDB_module().get_all_events()

    if 'username' in session:
        user_id = UsersDB_module().select_with_mail(mail=session['username'])['user_id']
        data_fav = FavoriteUsersDB_module().get_all_favorites_by_type_post(user_id, type_post)
        if data_fav:
            events = connect_events_with_favor(events=events, data_fav=data_fav)

    if request.method == 'POST':
        print(request.form.get('action'))
        print(request.form.get('action2'))
        action = request.form.get('action')
        if 'filter_go' in action:
            city_id = int(request.form.get('city').split("_")[-1])
            if city_id != 0:
                print(city_id, 'city')
                events = EventsDB_module().get_event_by_city_id(city_id=city_id)
                city_selected = f"{cities_list[city_id - 1][1]}"
                region_sel = f"{cities_list[city_id - 1][2]}"


            if 'checkbox_fav' in action:
                print(events)
                events = [item for item in events if item.get('view_status') == 1]

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

        if 'username' in session:
            data_fav = FavoriteUsersDB_module().get_all_favorites_by_type_post(user_id, type_post)
            events = connect_events_with_favor(events=events, data_fav=data_fav)



    return render_template('calendar.html', events=events, cities_list=cities_list,
                           city_selected=city_selected, region_sel=region_sel, msg_data=msg_data)