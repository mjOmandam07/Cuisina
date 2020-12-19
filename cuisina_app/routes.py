from flask import render_template, redirect, request, url_for, flash, jsonify
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
            flash('Chef Already Exist!', 'danger')
        elif db.validateEmail() == 2:
            flash('Chef Email Already Exist!', 'danger')
        else:
            db.addNewUser()
            user = db.viewUser()
            flash('Welcome to Cuisina Chef!', 'success')
            return redirect(url_for('profile', username=user[0][1]))
    return render_template('signUp.html', form=form)


@app.route('/home')
def home():
    flash('Welcome chef! You successfully entered the CUISINA')
    return render_template('home.html')



@app.route('/profile/<username>')
def profile(username):
    db = models.chef(username=username)
    user = db.viewUser()
    return render_template('profile.html', user = user)
    