from flask import render_template, redirect, request, url_for, flash, session
from cuisina_app import app
from cuisina_app.forms import LoginForm
import cuisina_app.models as models
from datetime import timedelta

app.permanent_session_lifetime = timedelta(days=2)


@app.route('/')
def toLogin():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db = models.chef()
    if form.validate_on_submit():
        session.permanent = True
        db = models.chef(username=form.username.data,
                         password=form.password.data)

        if db.validateLogin() == 1:
            flash('Invalid Login. Chef does not exist', 'danger')
        elif db.validateLogin() == 2:
            flash('Invalid Login. Wrong Password', 'danger')
        else:
            user = db.login()
            session['user'] = user
            return redirect(url_for('profile', user_id=user[0][0]))
    
    if 'user' in session:
        user = session['user']
        return redirect(url_for('profile', user_id=user[0][0]))


    return render_template('login.html', form=form)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user' in session:
        db = models.chef(user_id=user_id)
        user = db.viewUser()
        session['user'] = user
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
