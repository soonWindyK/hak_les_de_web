from flask import render_template, redirect, url_for, session
from databaseModules.classEventsDB import EventsDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from databaseModules.classCityRegionDB import CityRegionDB_module


def before_calendar():
    return calendar_()


def calendar_():
    cities_list = CityRegionDB_module().get_cities_list_with_region()

    events = False
    city_selected = region_sel = ''

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'filter_go':
            city_id = int(request.form.get('city').split("_")[-1])

            if city_id != 0:
                events = EventsDB_module().get_event_by_city_id(city_id=city_id)
                print(events)
                city_selected = f"{cities_list[city_id - 1][1]}"
                region_sel = f"{cities_list[city_id - 1][2]}"

    if events == False:
        events = EventsDB_module().get_all_events()


    return render_template('calendar.html', events=events, cities_list=cities_list,
                           city_selected=city_selected, region_sel=region_sel)