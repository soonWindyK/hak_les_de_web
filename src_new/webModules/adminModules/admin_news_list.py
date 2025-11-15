from flask import render_template, redirect, url_for, session
from databaseModules.classNewsDB import NewssDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from ..upload_file_from_flask import handle_file_upload
from databaseModules.classCityRegionDB import CityRegionDB_module


def before_admin_news():
    return admin_news_()


def admin_news_():
    news = NewssDB_module().get_all_news()
    print(news)
    return render_template('admin/admin-news-list.html', news=news)
