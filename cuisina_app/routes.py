import os
import secrets
from flask import render_template, redirect, request, url_for, flash, session
from datetime import timedelta
from cuisina_app import app
from PIL import Image
from cuisina_app.forms import LoginForm, SignUpForm, ProfileForm
import cuisina_app.models as models


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


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
  if 'user' in session:
    if session['user'][0][0] == user_id:
      clear = False
      db = models.chef(user_id = user_id)
      suggested_chef = db.suggestChef()
      user = db.currentUser()
      profile = db.checkProfile()
      form = ProfileForm()
      recipe = db.userRecipes()
      session['user'] = user 
      if not profile:
        db.addProfile()
      else:
        pass
      if form.validate_on_submit() and request.method == 'POST':
        update = models.chef(first_name=form.fname.data,
                             last_name=form.lname.data,
                              age=form.age.data,
                              gender=form.register_gender.data,
                              username=form.username.data,
                              email_address=form.email.data, user_id=user_id)
       
        if update.updt_validateUsername() == session['user'][0][1] and update.updt_validateEmail() == session['user'][0][2]:
          clear = True
        elif update.updt_validateUsername() != session['user'][0][1] and update.updt_validateUsername() != 1:
          flash('Chef Username Already Exist!', 'danger')
        elif update.updt_validateEmail() != session['user'][0][2] and update.updt_validateEmail() != 2:
          flash('Chef Email Already Exist!', 'danger')
        elif update.updt_validateUsername() == 1 or update.updt_validateEmail() == 2:
          clear = True


        if clear:
          update.updateUser()
          update.updateProfile() 
          if form.upload_picture.data:
            picture_file = save_profile_picture(form.upload_picture.data)
            picture = url_for('static', filename='profile_pics/' + picture_file)
            upload_picture = models.chef(filename = picture, user_id=user_id)
            upload_picture.uploadProfilePic()
          flash('Success! Profile Saved', 'success')

        return redirect(url_for('profile', user_id=user_id))
      elif request.method == "GET":
        if len(profile) != 0:
          form.fname.data = profile[0][1]
          form.lname.data = profile[0][2]
          form.age.data = profile[0][3]
          form.register_gender.data = profile[0][4]
        else:
          form.fname.data = None
          form.lname.data = None
          form.age.data = None
        form.username.data = user[0][1]
        form.email.data = user[0][2]
      return render_template('profile.html', form=form, user=user, recipe=recipe, suggested_chef = suggested_chef)
    else:
      flash('Please Logout and Login to your desired account', 'info')
      return redirect(url_for('login'))
  else:
    return redirect(url_for('login'))


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)


    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/viewProfile/<int:user_id>')
def viewProfile(user_id):
  if 'user' in session:
    db = models.chef(user_id = user_id)
    suggest = models.chef(user_id = session['user'][0][0])
    user = session['user']
    other_user = db.currentUser()
    profile = db.checkProfile()
    recipe = db.userRecipes()
    suggested_chef = suggest.suggestChef()
    return render_template('userProfile.html', user = user, other_user=other_user, recipe = recipe, profile = profile, suggested_chef = suggested_chef)

  else:
    return redirect(url_for('login'))




@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('login'))


