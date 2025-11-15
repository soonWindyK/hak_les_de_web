from flask import render_template, redirect, url_for, flash, session
from src_new.databaseModules.classKnowelegesDB import KnowelegesDB_module
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'static/uploads/courses'
ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'avi', 'mov', 'mkv', 'doc', 'docx', 'ppt', 'pptx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_courses_list(request):
    """Список всех курсов для администратора"""
    courses = KnowelegesDB_module().get_all_courses()
    return render_template('admin/admin-courses-list.html', courses=courses)


def admin_course_add(request):
    """Добавление нового курса"""
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        
        if not course_name:
            flash('Название курса обязательно', 'error')
            return render_template('admin/admin-course-add.html')

        course_id = KnowelegesDB_module().add_course(course_name)
        
        if course_id:
            flash('Курс успешно создан', 'success')
            return redirect(url_for('admin_course_detail', course_id=course_id))
        else:
            flash('Ошибка при создании курса', 'error')
    
    return render_template('admin/admin-course-add.html')


def admin_course_detail(request, course_id):
    """Детальная страница курса с темами"""

    course = KnowelegesDB_module().get_course_info(course_id)
    
    if not course:
        flash('Курс не найден', 'error')
        return redirect(url_for('admin_courses_list'))
    
    themes = KnowelegesDB_module().get_themses_by_course_id(course_id)
    return render_template('admin/admin-course-detail.html', course=course, themes=themes)


def admin_theme_add(request, course_id):
    """Добавление новой темы к курсу"""
    courses_db = CoursesDB_module()
    course = courses_db.get_course_by_id(course_id)
    
    if not course:
        flash('Курс не найден', 'error')
        return redirect(url_for('admin_courses_list'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        speaker = request.form.get('speaker')
        video_url = request.form.get('video_url')
        
        file_path = None
        
        # Обработка загрузки файла
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Создаем уникальное имя файла
                import time
                unique_filename = f"{int(time.time())}_{filename}"
                
                # Создаем папку если её нет
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                # Сохраняем относительный путь
                file_path = f"uploads/courses/{unique_filename}"
        
        if not title or not description or not speaker:
            flash('Заполните все обязательные поля', 'error')
            return render_template('admin/admin-theme-add.html', course=course)
        
        if not file_path and not video_url:
            flash('Необходимо загрузить файл или указать ссылку на видео', 'error')
            return render_template('admin/admin-theme-add.html', course=course)
        
        theme_id = courses_db.create_theme(
            title=title,
            description=description,
            courses_id=course_id,
            speaker=speaker,
            file_path=file_path,
            url=video_url
        )
        
        if theme_id:
            flash('Тема успешно добавлена', 'success')
            return redirect(url_for('admin_course_detail', course_id=course_id))
        else:
            flash('Ошибка при добавлении темы', 'error')
    
    return render_template('admin/admin-theme-add.html', course=course)


def admin_theme_edit(request, theme_id):
    """Редактирование темы"""
    courses_db = CoursesDB_module()
    theme = courses_db.get_theme_by_id(theme_id)
    
    if not theme:
        flash('Тема не найдена', 'error')
        return redirect(url_for('admin_courses_list'))
    
    course = courses_db.get_course_by_id(theme['courses_id'])
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        speaker = request.form.get('speaker')
        video_url = request.form.get('video_url')
        
        file_path = theme['file']  # Сохраняем старый путь
        
        # Обработка загрузки нового файла
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                import time
                unique_filename = f"{int(time.time())}_{filename}"
                
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                file_path = f"uploads/courses/{unique_filename}"
        
        if courses_db.update_theme(theme_id, title, description, speaker, file_path, video_url):
            flash('Тема успешно обновлена', 'success')
            return redirect(url_for('admin_course_detail', course_id=theme['courses_id']))
        else:
            flash('Ошибка при обновлении темы', 'error')
    
    return render_template('admin/admin-theme-edit.html', theme=theme, course=course)


def admin_theme_delete(request, theme_id):
    """Удаление темы"""
    courses_db = CoursesDB_module()
    theme = courses_db.get_theme_by_id(theme_id)
    
    if not theme:
        flash('Тема не найдена', 'error')
        return redirect(url_for('admin_courses_list'))
    
    course_id = theme['courses_id']
    
    if courses_db.delete_theme(theme_id):
        flash('Тема успешно удалена', 'success')
    else:
        flash('Ошибка при удалении темы', 'error')
    
    return redirect(url_for('admin_course_detail', course_id=course_id))
