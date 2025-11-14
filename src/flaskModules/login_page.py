from src.databaseModules.classUsersDB import UsersDB_module


def login_page(request):
    username = request.form['username']
    password = request.form['password']
    users = bd_users().select_po_us_name(username)
    # print(users)
    if 'id' in users:
        if users['password'] == password:
            flash(f'Welcome, {username}!', 'success_panel')
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return render_template('auth.html', message='Проблема с данными')
    else:
        return redirect(url_for('login', message='Проблема с данными'))

