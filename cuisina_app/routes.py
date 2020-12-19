from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
from cuisina_app.forms import SignUpForm
import cuisina_app.models as models




@app.route('/', methods=['GET', 'POST'])
def signUp():
    lastUser = users[-1]
    newUser = {}
    db = models.chef()
    form = SignUpForm()
    if form.validate_on_submit():
        db = models.chef(username = form.username.data,
                         email_address = str(form.email.data),
                         password = form.password.data)
        db.addNewUser()
        flash('Welcome to Cuisina Chef!', 'success')
        return redirect(url_for('profile', user_id=1))
    return render_template('signUp.html', form=form)


@app.route('/home')
def home():
    flash('Welcome chef! You successfully entered the CUISINA')
    return render_template('home.html')



@app.route('/profile/<int:user_id>')
def profile(user_id):
    db = models.chef(user_id=user_id)
    user = db.viewUser()
    return render_template('profile.html', user = user)
    