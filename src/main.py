import json, os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from databaseModules import *

app = Flask(__name__)
avatars_folder = os.path.join(os.path.dirname(__file__), 'avatars')
app.secret_key = 'your_secret_key_here'


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    from flaskModules.registration_page import reg_page
    if request.method == 'POST':
        return reg_page(request=request)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from flaskModules.login_page import login_page
    if request.method == 'POST':
        return login_page(request=request)

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
