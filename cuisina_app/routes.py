from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
from cuisina_app.forms import SignUpForm
import cuisina_app.models as models


class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


user = (User(email='admin@okay.com', username='ADMIN', password='password'))


@app.route('/', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.email.data == user.email and form.username.data == user.username and form.password.data == user.password:
            return redirect(url_for('home'))
    return render_template('signUp.html', form=form)


@app.route('/home')
def home():
    flash('Welcome chef! You successfully entered the CUISINA')
    return render_template('home.html')


# ADD THE ROUTE/ROUTES OF/FOR YOUR FEATURE
