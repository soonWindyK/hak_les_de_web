from databaseModules.classUsersDB import UsersDB_module
from databaseModules.classEventsDB import EventsDB_module
from src_new.databaseModules.classKnowelegesDB import KnowelegesDB_module
from webModules.hash_password_usr import hasher_pass
from flask import render_template, redirect, session, request, flash
from ..admin_checker import check_moderaotr


def before_moder_events_pending():
    if check_moderaotr():
        return moderator_events_pending_(mail=session['username'])



def moderator_events_pending_(mail):
    print(request, mail)

    msg = ''
    if request.method == "POST":
        to_do_status = 1
        action = request.form.get('action')
        if "true_nko" in action:
            to_do_status = 2
        if "false_nko" in action:
            to_do_status = 3

        nko_id = int(action.split("_")[-1])
        print(to_do_status, action, nko_id)

        if NkoDB_module().update_status_nko(nko_id=nko_id, status=to_do_status):
            msg = 'Успешно'
        else:
            msg = 'Ошибка удаления'

    events = EventsDB_module().get_all_nko(status=1)
    return render_template('moderator/moderator-events-pending.html', events=events)


