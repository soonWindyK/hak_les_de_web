from flask import render_template, redirect, url_for, session
from databaseModules.classKnowelegesDB import KnowelegesDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session

def before_courses(request):
    return courses_page(request=request)


def courses_page(request):
    courses_list = KnowelegesDB_module().get_all_courses()
    print(courses_list)
    return render_template('knowledge.html', courses=courses_list)


def course_detail_page(course_id):
    print(course_id)
    """Страница с темами курса"""
    course = KnowelegesDB_module().get_course_info(course_id)
    
    if not course:
        return redirect(url_for('knowledge'))

    themes = KnowelegesDB_module().get_themses_by_course_id(course_id)

    return render_template('course-detail.html', course=course, themes=themes)


def theme_detail_page(theme_id):
    """Страница просмотра темы"""

    theme = KnowelegesDB_module().get_theme_info(theme_id)
    print(theme)
    if not theme:
        return redirect(url_for('knowledge'))

    course = KnowelegesDB_module().get_course_info(theme['courses_id'])
    return render_template('theme-detail.html', theme=theme, course=course)
