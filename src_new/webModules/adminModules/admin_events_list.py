from flask import render_template, redirect, url_for, session
from databaseModules.classEventsDB import EventsDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from ..upload_file_from_flask import handle_file_upload
from databaseModules.classCityRegionDB import CityRegionDB_module


def before_admin_events():
    if 'username' in session:
        data_db = UsersDB_module().select_with_mail(mail=session['username'])
        if data_db['user_role'] == 2:
            return admin_events_()

    return redirect('/')


def admin_events_():
    print(request.form)
    events = EventsDB_module().get_all_events()

    if request.method == 'POST':
        action = request.form.get('action', None)
        if "event_" in action:
            event_id = int(action.split("_")[-1])

            if EventsDB_module().delete_event(event_id):
                print('Удалено')
                events = EventsDB_module().get_all_events()
            else:
                flash('Ивент не удалось удалить','error')

    return render_template('admin/admin-events-list.html', events=events)
