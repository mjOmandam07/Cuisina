from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
from cuisina_app.forms import LoginForm
import cuisina_app.models as models

user = [

    {
        'username': 'joeyabbe1234',
        'email_address': 'joey@yahoo.com',
        'user_id': '1',
        'password': '123'
    }

]


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == user[0]['username'] and form.password.data == user[0]['password']:
            flash('You have logged in', 'success')
        else:
            flash('Invalid Login. Please check username and password.', 'danger')
    return render_template('login.html', form=form)
