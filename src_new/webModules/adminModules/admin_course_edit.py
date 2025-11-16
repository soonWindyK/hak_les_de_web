from databaseModules.classUsersDB import UsersDB_module
from src_new.databaseModules.classKnowelegesDB import KnowelegesDB_module
from webModules.hash_password_usr import hasher_pass
from flask import render_template, redirect, session, request, flash


def before_admin_course_edit(course_id):
    if 'username' in session:
        return admin_edit_course(mail=session['username'], course_id=course_id)

    return redirect('/login')


def admin_edit_course(mail, course_id):
    print(request, mail, course_id)
    text_course = KnowelegesDB_module().get_course_info(id=course_id)['name']
    if request.method == "POST":
        action = request.form.get('action')
        if action == 'save_course_name':
            new_name = request.form['name']
            if new_name == text_course:
                return render_template('admin/admin-course-edit.html', text_course=new_name, success='Изменения уже внесены')

            if KnowelegesDB_module().update_course(course_id=course_id, new_name=new_name):
                return render_template('admin/admin-course-edit.html', text_course=new_name, success='Успешно')
            else:
                return render_template('admin/admin-course-edit.html', text_course=text_course, success='Ошибка')


    return render_template('admin/admin-course-edit.html', text_course=text_course)



