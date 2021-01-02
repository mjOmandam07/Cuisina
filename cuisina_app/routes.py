from flask import render_template, redirect, request, url_for, flash
from cuisina_app import app
from cuisina_app.forms import SignUpForm
import cuisina_app.models as models



@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    newUser = {}
    db = models.chef()
    form = SignUpForm()
    if form.validate_on_submit():
        db = models.chef(username = form.username.data,
                         email_address = str(form.email.data),
                         password = form.password.data)
        if db.validateUsername() == 1:
            flash('Chef Username Already Exist!', 'danger')
        elif db.validateEmail() == 2:
            flash('Chef Email Already Exist!', 'danger')
        else:
            db.addNewUser()
            session.permanent = True
            login = models.chef(username=form.username.data,
                            password=form.password.data)
            user = login.login()
            session['user'] = user
            return redirect(url_for('profile', user_id=user[0][0]))
            flash('Welcome to Cuisina Chef!', 'success')
    return render_template('signUp.html', form=form)




@app.route('/profile/<int:user_id>')
def profile(user_id):
    db = models.chef(user_id=user_id)
    user = db.viewUser()
    return render_template('profile.html', user=user)
    