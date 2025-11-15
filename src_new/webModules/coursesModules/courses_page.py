from flask import render_template, redirect, url_for, session
from databaseModules.classCoursesDB import CoursesDB_module


def courses_list_page():
    """Страница со списком курсов"""
    courses_db = CoursesDB_module()
    courses = courses_db.get_all_courses()
    return render_template('knowledge.html', courses=courses)


def course_detail_page(course_id):
    """Страница с темами курса"""
    courses_db = CoursesDB_module()
    course = courses_db.get_course_by_id(course_id)
    
    if not course:
        return redirect(url_for('knowledge'))
    
    courses_db2 = CoursesDB_module()
    themes = courses_db2.get_themes_by_course(course_id)
    print(f"Course ID: {course_id}, Themes found: {len(themes)}")
    print(f"Themes data: {themes}")
    return render_template('course-detail.html', course=course, themes=themes)


def theme_detail_page(theme_id):
    """Страница просмотра темы"""
    courses_db = CoursesDB_module()
    theme = courses_db.get_theme_by_id(theme_id)
    
    if not theme:
        return redirect(url_for('knowledge'))
    
    course = courses_db.get_course_by_id(theme['courses_id'])
    return render_template('theme-detail.html', theme=theme, course=course)
