from flask import render_template, redirect, url_for, session
from databaseModules.classEventsDB import EventsDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request


def before_calendar():
    return calendar_()


def calendar_():
    events = EventsDB_module().get_all_events()
    return render_template('calendar.html', events=events)