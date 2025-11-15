from flask import render_template, redirect, url_for, session
from databaseModules.classNewsDB import NewssDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from ..upload_file_from_flask import handle_file_upload
from databaseModules.classCityRegionDB import CityRegionDB_module


def before_news():
    return news_()


def news_():
    news = NewssDB_module().get_all_news()
    return render_template('news.html', news=news)
