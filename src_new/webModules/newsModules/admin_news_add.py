from flask import render_template, redirect, url_for, session
from databaseModules.classNewsDB import NewssDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from ..upload_file_from_flask import handle_file_upload
from databaseModules.classCityRegionDB import CityRegionDB_module



def before_admin_new_add():
    if 'username' in session:
        data_db = UsersDB_module().select_with_mail(mail=session['username'])
        if data_db['user_role'] == 2:
            return admin_news_add()
        else:
            return redirect('/news')

    return redirect('/login')


def admin_news_add():
    print("Request:", request)
    print("Method:", request.method)
    print("Form data:", request.form)
    print("Files:", request.files)
    cities_list = CityRegionDB_module().get_cities_list_with_region()
    if request.method == 'POST':
        try:
            # Обрабатываем загрузку ПРИКРЕПЛЕННЫХ ФАЙЛОВ
            attached_success, attached_result = handle_file_upload('avatar')

            attached_path = None
            if attached_success:
                attached_path = attached_result
                print(f"Прикрепленный файл сохранен: {attached_path}")
            else:
                print(f"Прикрепленный файл: {attached_result}")

            # Получаем данные из формы
            data = {
                'title': request.form.get('title', ''),
                'description': request.form.get('description', ''),
                'created_by_id': None,
                'attached_path': attached_path,
                'city': request.form.get('city', ''),
            }

            data['city'] = data['city'].split("_")[-1]
            data['created_by_id'] = UsersDB_module().select_with_mail(mail=session['username'])['user_id']
            print("Form data received:", data)

            # Проверяем обязательные поля
            if not data['title'] or not data['description'] or not data['city']:
                flash("Заполните все обязательные поля", "error")
                return render_template('admin/admin-news-add.html')

            # логика сохранения в БД
            NewssDB_module().create_new(data=list(data.values()))

            flash("Новость успешно добавлена!", "success")
            return redirect(url_for('admin_news_list'))

        except Exception as e:
            print(f"Ошибка при добавлении новости: {str(e)}")
            flash(f"Ошибка при добавлении новости: {str(e)}", "error")

    return render_template('admin/admin-news-add.html', cities_list=cities_list)