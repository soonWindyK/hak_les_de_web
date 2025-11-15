from flask import render_template, redirect, url_for, session
from databaseModules.classEventsDB import EventsDB_module
from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session, flash, request
from databaseModules.classCityRegionDB import CityRegionDB_module



def before_admin_event_add():
    if 'username' in session:
        data_db = UsersDB_module().select_with_mail(mail=session['username'])
        if data_db['user_role'] == 2:
            return admin_news_add()
        else:
            return redirect('/news')

    return redirect('/')


def admin_news_add():
    cities_list = CityRegionDB_module().get_cities_list_with_region()

    if request.method == 'POST':
        try:
            # Получаем данные из формы
            data_from = {
                'title': request.form.get('title', ''),
                'description': request.form.get('description', ''),
                'organizer': request.form.get('organizer', ''),
                'location': request.form.get('location', ''),
                'date': request.form.get('date', ''),
                'city': request.form.get('city', ''),
                "category_id": 5,
                'time_start': request.form.get('time_start', ''),
                'time_end': request.form.get('time_end', ''),
                'creator_id': UsersDB_module().select_with_mail(mail=session['username'])['user_id']
            }
            data_from['city'] = data_from['city'].split("_")[-1]

            print("Данные формы:", data_from)

            # ПРОВЕРКА ВРЕМЕНИ
            if data_from['time_start'] >= data_from['time_end']:
                return render_template('admin/admin-events-add.html', cities_list=cities_list, data_from=data_from,
                    error_msg='Время начала должно быть раньше времени окончания')

            if data_from['city'] == '0':
                return render_template('admin/admin-events-add.html', cities_list=cities_list, data_from=data_from,
                    error_msg='Выберите город')

            data_from['date'] = data_from['date']  # '2025-11-29' - дата события (без времени)
            data_from['time_start'] = f"{data_from['date']} {data_from['time_start']}:00"  # '2025-11-29 16:44:00'
            data_from['time_end'] = f"{data_from['date']} {data_from['time_end']}:00"  # '2025-11-29 1

            print("Данные формы:", data_from)
            #  логика сохранения в БД
            EventsDB_module().create_event(data=list(data_from.values()))

            flash("Событие успешно создано!", "success")
            return redirect(url_for('admin_events_list'))

        except Exception as e:
            print(f"Ошибка при создании события: {str(e)}")
            flash(f"Ошибка при создании события: {str(e)}", "error")
            return render_template('admin/admin-events-add.html', cities_list=cities_list, data_from=data_from)

    # Предзаполняем cities для выпадающего списка
    return render_template('admin/admin-events-add.html', cities_list=cities_list)